# Copyright (c) 2026 NightWorksIO
"""Carrying out an action a key may call: rehearsing it, asking for it, following its job to the end, and saying what became of it.

An action whose rehearsal answers an offer is asked for with that offer, so
the stack refuses it where what it would do has moved since. Every outcome is
fired as a `lemonfiber_job` event, and a failure is raised in the stack's own
words, so a control reports the job it started either way.
"""

from enum import StrEnum
from typing import TYPE_CHECKING, Final

from homeassistant.exceptions import HomeAssistantError
from lemonfiber import KEY_CALLABLE, Ended, LemonfiberError, NotAdmittedError, expect, is_key_callable

from .connection import refused
from .const import DOMAIN

if TYPE_CHECKING:
    from collections.abc import Mapping

    from homeassistant.core import HomeAssistant
    from lemonfiber import AsyncClient, Json

    from .runtime import LemonfiberConfigEntry

JOB_EVENT: Final = f"{DOMAIN}_job"
"""The event every outcome of an action is fired as."""

DRY_RUN: Final = "dry_run"
"""The argument that asks for a rehearsal: what the action would do, with none of it done."""

OFFER: Final = "offer"
"""Where a rehearsal names what it would do, and the real call carries it back."""

JOB: Final = "job"
"""The kind an action answers with when it started work that outlives the request."""


class Outcome(StrEnum):
    """What became of an action."""

    FINISHED = "finished"
    """The work finished."""
    ENDED = "ended"
    """The work ended before it finished: its name was released, or nothing asked after it."""
    FAILED = "failed"
    """The stack refused the action, or the work failed."""


async def offered(client: AsyncClient, action: str, arguments: Mapping[str, Json] | None) -> dict[str, Json]:
    """Return an action's arguments with the offer its rehearsal answered, for an action that answers one.

    The stack refuses the call where what it would do has moved since the
    rehearsal, so what is carried out is what was rehearsed. An action that
    answers no offer is called with its arguments as they are.
    """
    asked: dict[str, Json] = dict(arguments or {})
    if not is_key_callable(action) or KEY_CALLABLE[action].moved is None:
        return asked
    rehearsal = (await client.act(action, {**asked, DRY_RUN: True}))["data"]
    offer = rehearsal.get(OFFER) if isinstance(rehearsal, dict) else None
    if isinstance(offer, str):
        asked[OFFER] = offer
    return asked


async def carry_out(
    hass: HomeAssistant,
    entry: LemonfiberConfigEntry,
    action: str,
    arguments: Mapping[str, Json] | None = None,
) -> Outcome:
    """Ask the stack for an action, follow any job it starts to the end, fire what became of it, and return that.

    A failure is fired too, and then raised as the stack's own sentence; a refused
    key also asks for a new one.
    """
    client = entry.runtime_data.connected.client
    said: dict[str, str] = {"entry_id": entry.entry_id, "action": action}
    try:
        answer = await client.act(action, await offered(client, action, arguments))
        outcome = Outcome.FINISHED
        if answer["kind"] == JOB:
            started = expect(answer, JOB)
            said["job"] = started["data"]["job"]
            if isinstance(await client.follow(started), Ended):
                outcome = Outcome.ENDED
    except LemonfiberError as error:
        refusal = refused(error)
        hass.bus.async_fire(JOB_EVENT, {**said, "outcome": Outcome.FAILED, **refusal.placeholders})
        if isinstance(error, NotAdmittedError):
            entry.async_start_reauth(hass)
        raise HomeAssistantError(
            translation_domain=DOMAIN,
            translation_key=refusal.reason,
            translation_placeholders=dict(refusal.placeholders),
        ) from error
    hass.bus.async_fire(JOB_EVENT, {**said, "outcome": outcome})
    return outcome
