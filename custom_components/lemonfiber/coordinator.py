# Copyright (c) 2026 NightWorksIO
"""The stack as Home Assistant follows it: the dashboard and the alerts from the event stream, the doctor's findings and the services' versions by read."""

import asyncio
from abc import abstractmethod
from dataclasses import dataclass
from enum import StrEnum
from functools import partial
from typing import TYPE_CHECKING, Final, override

from homeassistant.core import CALLBACK_TYPE, callback
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from lemonfiber import Gap, LemonfiberError, Live, NotAdmittedError, Read, expect

from .alerts import alert_in, fire
from .connection import NotConnectedError, Reason, refused, scope_of
from .const import DIAGNOSIS_EVERY, DOMAIN, FIRST_SNAPSHOT_WITHIN, LOGGER, VERSIONS_EVERY

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from homeassistant.core import HomeAssistant
    from lemonfiber import Arrival, AsyncClient, AsyncStream
    from lemonfiber.contract import Alert, DoctorReport, PlayingReport, Snapshot, UpdateChange

    from .connection import Connected
    from .runtime import LemonfiberConfigEntry

DASHBOARD: Final = "dashboard"
"""The kind the stream carries the dashboard in."""

PLAYING: Final = "playing"
"""The kind a stream carries what is playing in: every session on the stack's, a member's own on theirs."""

STACK: Final = {"what": "stack"}
"""What the `update` read is asked about: the services the stack runs, rather than lemonfiber itself."""


class State(StrEnum):
    """Where an entry stands with its stack, as F12 names the four."""

    CONNECTED = "connected"
    """The stream is live and the entities are current."""
    STALE = "stale"
    """The stream has a gap; the entities it built show unavailable until it resumes."""
    REFUSED = "refused"
    """The key was refused; reauthentication has been asked for."""
    UNREACHABLE = "unreachable"
    """The stack did not answer at the address, or the pin did not match."""


def dashboard_in(arrival: Arrival) -> Snapshot | None:
    """Return the dashboard an arrival carries live, or None where it is anything else."""
    if not isinstance(arrival, Live) or arrival.envelope["kind"] != DASHBOARD:
        return None
    return expect(arrival.envelope, DASHBOARD)["data"]


def playing_in(arrival: Arrival) -> PlayingReport | None:
    """Return what is playing as an arrival carries it live, or None where it is anything else."""
    if not isinstance(arrival, Live) or arrival.envelope["kind"] != PLAYING:
        return None
    return expect(arrival.envelope, PLAYING)["data"]


async def first_snapshot(stream: AsyncStream) -> Snapshot:
    """Return the first dashboard the stream carries live, closing the stream where none arrives in time."""
    try:
        async with asyncio.timeout(FIRST_SNAPSHOT_WITHIN):
            while True:
                if (snapshot := dashboard_in(await anext(stream))) is not None:
                    return snapshot
    except TimeoutError:
        await stream.aclose()
        raise NotConnectedError(Reason.NO_DASHBOARD) from None
    except LemonfiberError as error:
        await stream.aclose()
        raise refused(error) from None


class DiagnosisCoordinator(DataUpdateCoordinator["DoctorReport | None"]):
    """The doctor's findings, read hourly and whenever the stream says the stack's health moved."""

    config_entry: LemonfiberConfigEntry

    def __init__(self, hass: HomeAssistant, entry: LemonfiberConfigEntry, client: AsyncClient) -> None:
        """Read the findings through the entry's client."""
        super().__init__(
            hass,
            LOGGER,
            config_entry=entry,
            name=f"{DOMAIN} diagnosis",
            update_interval=DIAGNOSIS_EVERY,
        )
        self._client = client

    @override
    async def _async_update_data(self) -> DoctorReport:
        try:
            return expect(await self._client.read(Read.CHECKS), "doctor")["data"]
        except LemonfiberError as error:
            raise read_failed(error) from error


def read_failed(error: LemonfiberError) -> ConfigEntryAuthFailed | UpdateFailed:
    """Return what a coordinator raises when a read fails: a refused key, or a reading that did not arrive."""
    if isinstance(error, NotAdmittedError):
        return ConfigEntryAuthFailed(translation_domain=DOMAIN, translation_key=Reason.KEY_REFUSED)
    refusal = refused(error)
    return UpdateFailed(
        translation_domain=DOMAIN,
        translation_key=refusal.reason,
        translation_placeholders=dict(refusal.placeholders),
    )


@dataclass(frozen=True, slots=True)
class Versions:
    """The version of each service the stack runs: the tag this build pins, and the step to it where one is owed."""

    pinned: Mapping[str, str]
    """Each service's id, to the tag this build of lemonfiber pins it at."""
    changes: Mapping[str, UpdateChange]
    """Each service's id, to what updating it would change, for every service that is not on its pin."""

    def installed(self, service: str) -> str | None:
        """Return the tag a service stands on, or None where the stack names no version for it."""
        change = self.changes.get(service)
        return self.pinned.get(service) if change is None else change["current"]


class VersionsCoordinator(DataUpdateCoordinator["Versions | None"]):
    """The version of every service, read hourly from where the services come from and what updating would move."""

    config_entry: LemonfiberConfigEntry

    def __init__(self, hass: HomeAssistant, entry: LemonfiberConfigEntry, client: AsyncClient) -> None:
        """Read the versions through the entry's client."""
        super().__init__(
            hass,
            LOGGER,
            config_entry=entry,
            name=f"{DOMAIN} versions",
            update_interval=VERSIONS_EVERY,
        )
        self._client = client

    @override
    async def _async_update_data(self) -> Versions:
        try:
            provenance = expect(await self._client.read(Read.PROVENANCE), "provenance")["data"]
            update = expect(await self._client.read(Read.UPDATE, STACK), "update")["data"]
        except LemonfiberError as error:
            raise read_failed(error) from error
        return Versions(
            pinned={service["id"]: service["pinned"] for service in provenance["services"]},
            changes={change["service"]: change for change in update["changes"]},
        )


class Following[T](DataUpdateCoordinator[T]):
    """What the entry's event stream last said, unavailable from a gap until the stream says it again.

    A stream ends one of two ways: a refused key asks for reauthentication, and
    a lost stack reloads the entry, whose setup is retried with Home Assistant's
    backoff and reads the key's scope again when it reaches the stack.
    """

    config_entry: LemonfiberConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        entry: LemonfiberConfigEntry,
        connected: Connected,
        stream: AsyncStream,
        first: T,
    ) -> None:
        """Hold the open stream and what it said first."""
        super().__init__(hass, LOGGER, config_entry=entry, name=f"{DOMAIN} stream")
        self.data = first
        self.state = State.CONNECTED
        self._connected = connected
        self._stream = stream

    async def follow(self) -> None:
        """Follow the stream until the key is refused or the stack is lost, then hand the entry back to Home Assistant."""
        try:
            while True:
                arrival = await anext(self._stream)
                if isinstance(arrival, Gap):
                    self._lost(State.STALE)
                else:
                    self._heard(arrival)
        except NotAdmittedError:
            self._lost(State.REFUSED)
            self.config_entry.async_start_reauth(self.hass)
        except LemonfiberError:
            self._lost(State.UNREACHABLE)
            self.hass.config_entries.async_schedule_reload(self.config_entry.entry_id)

    @abstractmethod
    def _heard(self, arrival: Arrival) -> None:
        """Take in one arrival that is not a gap."""

    def _carried(self, data: T) -> None:
        if self.state is State.STALE:
            LOGGER.info("The stream from %s resumed", self.config_entry.title)
            self.config_entry.async_create_background_task(self.hass, self._rescope(), f"{DOMAIN} scope")
        self.state = State.CONNECTED
        self.async_set_updated_data(data)

    def _lost(self, state: State) -> None:
        if self.state is State.CONNECTED:
            LOGGER.info(
                "The stream from %s is %s; its entities are unavailable",
                self.config_entry.title,
                state,
            )
        self.state = state
        self.last_update_success = False
        self.async_update_listeners()

    async def _rescope(self) -> None:
        """Read the key's scope again after a gap, and reload the entry where it changed."""
        try:
            capabilities = await self._connected.client.capabilities()
        except LemonfiberError:
            return
        try:
            moved = scope_of(capabilities) is not self._connected.scope
        except NotConnectedError:
            moved = True
        if moved:
            self.hass.config_entries.async_schedule_reload(self.config_entry.entry_id)


class StreamCoordinator(Following["Snapshot"]):
    """The dashboard and what is playing as the event stream carries them, and each alert it carries fired.

    What is playing is held apart from the dashboard: it is None until the
    stream says it, and again from a gap until the stream says it again.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        entry: LemonfiberConfigEntry,
        connected: Connected,
        stream: AsyncStream,
        first: Snapshot,
    ) -> None:
        """Hold the open stream and the first dashboard it carried, and the findings it asks to be read again."""
        super().__init__(hass, entry, connected, stream, first)
        self.diagnosis = DiagnosisCoordinator(hass, entry, connected.client)
        self._alert_listeners: list[Callable[[Alert], None]] = []
        self.playing: PlayingReport | None = None

    @callback
    def async_add_alert_listener(self, listener: Callable[[Alert], None]) -> CALLBACK_TYPE:
        """Call a listener with every alert the stream carries from now on, until the returned callback is called."""
        self._alert_listeners.append(listener)
        return partial(self._alert_listeners.remove, listener)

    @override
    def _heard(self, arrival: Arrival) -> None:
        if (snapshot := dashboard_in(arrival)) is not None:
            moved = snapshot["health"] != self.data["health"]
            self._carried(snapshot)
            if moved:
                self.config_entry.async_create_background_task(
                    self.hass,
                    self.diagnosis.async_request_refresh(),
                    f"{DOMAIN} diagnosis",
                )
        elif (playing := playing_in(arrival)) is not None:
            self.playing = playing
            self.async_update_listeners()
        elif (alert := alert_in(arrival)) is not None:
            fire(self.hass, self.config_entry, alert)
            for listener in tuple(self._alert_listeners):
                listener(alert)

    @override
    def _lost(self, state: State) -> None:
        self.playing = None
        super()._lost(state)
