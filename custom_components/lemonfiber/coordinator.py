# Copyright (c) 2026 NightWorksIO
"""The stack as Home Assistant follows it: the dashboard from the event stream, and the doctor's findings by read."""

import asyncio
from enum import StrEnum
from typing import TYPE_CHECKING, Final, override

from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from lemonfiber import Gap, LemonfiberError, Live, NotAdmittedError, Read, expect

from .connection import NotConnectedError, Reason, refused, scope_of
from .const import DIAGNOSIS_EVERY, DOMAIN, FIRST_SNAPSHOT_WITHIN, LOGGER

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from lemonfiber import AsyncClient, AsyncStream, Envelope
    from lemonfiber.contract import DoctorReport, Snapshot

    from .connection import Connected
    from .runtime import LemonfiberConfigEntry

DASHBOARD: Final = "dashboard"
"""The kind the stream carries the dashboard in."""


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


def dashboard_in(envelope: Envelope) -> Snapshot | None:
    """Return the dashboard an envelope carries, or None where it carries another kind."""
    return expect(envelope, DASHBOARD)["data"] if envelope["kind"] == DASHBOARD else None


async def first_snapshot(stream: AsyncStream) -> Snapshot:
    """Return the first dashboard the stream carries live, closing the stream where none arrives in time."""
    try:
        async with asyncio.timeout(FIRST_SNAPSHOT_WITHIN):
            while True:
                match await anext(stream):
                    case Live(envelope) if (snapshot := dashboard_in(envelope)) is not None:
                        return snapshot
                    case _:
                        pass
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
        super().__init__(hass, LOGGER, config_entry=entry, name=f"{DOMAIN} diagnosis", update_interval=DIAGNOSIS_EVERY)
        self._client = client

    @override
    async def _async_update_data(self) -> DoctorReport:
        try:
            return expect(await self._client.read(Read.CHECKS), "doctor")["data"]
        except NotAdmittedError as error:
            raise ConfigEntryAuthFailed(translation_domain=DOMAIN, translation_key=Reason.KEY_REFUSED) from error
        except LemonfiberError as error:
            refusal = refused(error)
            raise UpdateFailed(
                translation_domain=DOMAIN,
                translation_key=refusal.reason,
                translation_placeholders=dict(refusal.placeholders),
            ) from error


class StreamCoordinator(DataUpdateCoordinator["Snapshot"]):
    """The dashboard as the event stream carries it, unavailable from a gap until the stream says it again."""

    config_entry: LemonfiberConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        entry: LemonfiberConfigEntry,
        connected: Connected,
        stream: AsyncStream,
        first: Snapshot,
    ) -> None:
        """Hold the open stream and the first dashboard it carried, and the findings it asks to be read again."""
        super().__init__(hass, LOGGER, config_entry=entry, name=f"{DOMAIN} stream")
        self.data = first
        self.state = State.CONNECTED
        self.diagnosis = DiagnosisCoordinator(hass, entry, connected.client)
        self._connected = connected
        self._stream = stream

    async def follow(self) -> None:
        """Follow the stream until the key is refused or the stack is lost, then hand the entry back to Home Assistant.

        A refused key asks for reauthentication. A lost stack reloads the entry,
        whose setup is retried with Home Assistant's backoff and reads the key's
        scope again when it reaches the stack.
        """
        try:
            while True:
                match await anext(self._stream):
                    case Live(envelope) if (snapshot := dashboard_in(envelope)) is not None:
                        self._carried(snapshot)
                    case Gap():
                        self._lost(State.STALE)
                    case _:
                        pass
        except NotAdmittedError:
            self._lost(State.REFUSED)
            self.config_entry.async_start_reauth(self.hass)
        except LemonfiberError:
            self._lost(State.UNREACHABLE)
            self.hass.config_entries.async_schedule_reload(self.config_entry.entry_id)

    def _carried(self, snapshot: Snapshot) -> None:
        resumed = self.state is State.STALE
        moved = snapshot["health"] != self.data["health"]
        if resumed:
            LOGGER.info("The stream from %s resumed", self.config_entry.title)
            self.config_entry.async_create_background_task(self.hass, self._rescope(), f"{DOMAIN} scope")
        self.state = State.CONNECTED
        self.async_set_updated_data(snapshot)
        if moved:
            self.config_entry.async_create_background_task(
                self.hass, self.diagnosis.async_request_refresh(), f"{DOMAIN} diagnosis"
            )

    def _lost(self, state: State) -> None:
        if self.state is State.CONNECTED:
            LOGGER.info("The stream from %s is %s; its entities are unavailable", self.config_entry.title, state)
        self.state = state
        self.last_update_success = False
        self.async_update_listeners()

    async def _rescope(self) -> None:
        """Read the key's scope again after a gap, and reload the entry where it changed."""
        try:
            capabilities = await self._connected.client.capabilities()
        except LemonfiberError:
            return
        if scope_of(capabilities) is not self._connected.scope:
            self.hass.config_entries.async_schedule_reload(self.config_entry.entry_id)
