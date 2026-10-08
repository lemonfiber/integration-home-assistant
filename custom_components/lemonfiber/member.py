# Copyright (c) 2026 NightWorksIO
"""A member's own side of the stack, from the stream the stack opens for their key alone.

That stream carries their row of the household, their shelf and what they are
playing, each as their own read answers it, and nothing gathered for the
operator. What it said of each is held apart: after a gap, each is unknown
until the stream says it again.
"""

import asyncio
import typing
from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, Final, override

from lemonfiber import LemonfiberError, Live, expect
from lemonfiber.contract import RequestState

from .connection import NotConnectedError, Reason, refused
from .const import FIRST_SNAPSHOT_WITHIN
from .coordinator import Following, State

if TYPE_CHECKING:
    from lemonfiber import Arrival, AsyncStream
    from lemonfiber.contract import HouseholdReport, MemberRequest, Playback, PlayingReport

HOUSEHOLD: Final = "household"
"""The kind a member's stream carries their row of the household in."""

PLAYING: Final = "playing"
"""The kind a member's stream carries what they are playing in."""

REQUEST_STATES: Final[tuple[RequestState, ...]] = typing.get_args(RequestState.__value__)
"""Every state a request can stand at, in the order a request moves through them."""

GONE: Final = "gone"
"""The state of a request whose title has left the media server, counted by an entity left off until enabled."""


@dataclass(frozen=True, slots=True)
class Theirs:
    """What a member's stream last said of their household row and of what they are playing, or None until it says it."""

    household: HouseholdReport | None = None
    playing: PlayingReport | None = None

    @property
    def complete(self) -> bool:
        """Tell whether the stream has said both."""
        return self.household is not None and self.playing is not None

    def requests(self, state: RequestState) -> list[MemberRequest] | None:
        """Return their requests that stand at a state, newest first, or None where their row cannot be read."""
        if self.household is None or not self.household["available"]:
            return None
        return [
            request
            for member in self.household["members"]
            for request in member["requests"]
            if request.get("state") == state
        ]

    def sessions(self) -> list[Playback] | None:
        """Return what they are playing now, or None where the media server could not say."""
        if self.playing is None or not self.playing["available"]:
            return None
        return self.playing["sessions"]


def heard(theirs: Theirs, arrival: Arrival) -> Theirs | None:
    """Return what the member's side comes to with an arrival, or None where it carries nothing of theirs."""
    if not isinstance(arrival, Live):
        return None
    if arrival.envelope["kind"] == HOUSEHOLD:
        return replace(theirs, household=expect(arrival.envelope, HOUSEHOLD)["data"])
    if arrival.envelope["kind"] == PLAYING:
        return replace(theirs, playing=expect(arrival.envelope, PLAYING)["data"])
    return None


async def first_theirs(stream: AsyncStream) -> Theirs:
    """Return the member's side once their stream has said both, closing the stream where it does not in time."""
    theirs = Theirs()
    try:
        async with asyncio.timeout(FIRST_SNAPSHOT_WITHIN):
            while not theirs.complete:
                theirs = heard(theirs, await anext(stream)) or theirs
    except TimeoutError:
        await stream.aclose()
        raise NotConnectedError(Reason.NOTHING_SAID) from None
    except LemonfiberError as error:
        await stream.aclose()
        raise refused(error) from None
    return theirs


class MemberCoordinator(Following[Theirs]):
    """A member's household row and what they are playing, as their stream carries them."""

    @override
    def _heard(self, arrival: Arrival) -> None:
        if (theirs := heard(self.data, arrival)) is not None:
            self._carried(theirs)

    @override
    def _lost(self, state: State) -> None:
        self.data = Theirs()
        super()._lost(state)
