# Copyright (c) 2026 NightWorksIO
"""The controls an `act` key gets without a rehearsal: running the doctor, and pausing or resuming downloads."""

from typing import TYPE_CHECKING, Final, cast

import pytest
from homeassistant.const import ATTR_ASSUMED_STATE, ATTR_ENTITY_ID, STATE_OFF, STATE_ON, STATE_UNKNOWN
from homeassistant.exceptions import HomeAssistantError
from pytest_homeassistant_custom_component.common import async_capture_events

from custom_components.lemonfiber.connection import Reason
from custom_components.lemonfiber.jobs import JOB_EVENT
from tests.conftest import DIAGNOSIS, capabilities, reauthenticating, serve, until
from tests.stack import Reply, envelope, problem

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from pytest_homeassistant_custom_component.common import MockConfigEntry

    from tests.stack import Stack

DOCTOR: Final = "button.127_0_0_1_run_the_doctor"
PAUSED: Final = "switch.127_0_0_1_downloads_paused"
STARTED: Final = Reply(202, envelope("job", {"action": "diagnose", "job": "j-1"}))
PAUSING: Final = Reply(body=envelope("pausing", {"asked": "pause", "clients": [], "rehearsed": False}))


async def set_up(hass: HomeAssistant, entry: MockConfigEntry) -> None:
    """Set the entry up and let everything it started settle."""
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    await until(hass, lambda: entry.runtime_data.technical.diagnosis.data is not None)


def state(hass: HomeAssistant, entity_id: str) -> str:
    """Return an entity's state."""
    held = hass.states.get(entity_id)
    assert held is not None
    return held.state


async def press(hass: HomeAssistant) -> None:
    """Press the doctor's button and wait for what it started."""
    await hass.services.async_call("button", "press", {ATTR_ENTITY_ID: DOCTOR}, blocking=True)


async def test_a_read_key_gets_no_control(hass: HomeAssistant, stack: Stack, entry: MockConfigEntry) -> None:
    serve(stack)
    await set_up(hass, entry)
    assert hass.states.get(DOCTOR) is hass.states.get(PAUSED) is None


async def test_a_control_whose_action_is_switched_off_is_not_created(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack, "act")
    switched_off = capabilities("act")
    states = cast("dict[str, dict[str, str]]", switched_off["data"])["capabilities"]
    states["/api/actions/diagnose"] = "unconfigured"
    states["/api/actions/downloads-resume"] = "unpermitted"
    stack.reply("/api/capabilities", Reply(body=switched_off))
    await set_up(hass, entry)
    assert hass.states.get(DOCTOR) is hass.states.get(PAUSED) is None


async def test_running_the_doctor_follows_its_job_and_reads_the_findings_again(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack, "act")
    stack.reply("/api/actions/diagnose", STARTED)
    stack.reply("/api/jobs/j-1", Reply(body=DIAGNOSIS))
    await set_up(hass, entry)
    fired = async_capture_events(hass, JOB_EVENT)
    await press(hass)
    assert [event.data for event in fired] == [
        {"entry_id": entry.entry_id, "action": "diagnose", "job": "j-1", "outcome": "finished"},
    ]
    await until(hass, lambda: stack.asked("/api/checks") == 2)


async def test_a_job_that_ended_before_it_finished_says_so(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack, "act")
    stack.reply("/api/actions/diagnose", STARTED)
    stack.reply("/api/jobs/j-1", Reply(body=STARTED.body))
    await set_up(hass, entry)
    fired = async_capture_events(hass, JOB_EVENT)
    await press(hass)
    assert fired[0].data["outcome"] == "ended"


async def test_an_action_answered_at_once_has_no_job_to_follow(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack, "act")
    stack.reply("/api/actions/diagnose", Reply(body=DIAGNOSIS))
    await set_up(hass, entry)
    fired = async_capture_events(hass, JOB_EVENT)
    await press(hass)
    assert [event.data for event in fired] == [
        {"entry_id": entry.entry_id, "action": "diagnose", "outcome": "finished"},
    ]


async def test_a_refused_action_is_said_in_the_stacks_words_and_fired(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack, "act")
    stack.reply("/api/actions/diagnose", Reply(409, problem("BUSY-1", "A repair is running.")))
    await set_up(hass, entry)
    fired = async_capture_events(hass, JOB_EVENT)
    with pytest.raises(HomeAssistantError) as raised:
        await press(hass)
    assert raised.value.translation_key == Reason.REFUSED
    assert raised.value.translation_placeholders == {"sentence": "A repair is running."}
    assert fired[0].data == {
        "entry_id": entry.entry_id,
        "action": "diagnose",
        "outcome": "failed",
        "sentence": "A repair is running.",
    }


async def test_a_key_refused_on_a_press_asks_for_a_new_one(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack, "act")
    stack.reply("/api/actions/diagnose", Reply(403, problem("ADMIT-4", "Not admitted.")))
    await set_up(hass, entry)
    with pytest.raises(HomeAssistantError):
        await press(hass)
    await until(hass, lambda: reauthenticating(hass))


async def test_the_downloads_switch_shows_what_it_last_asked_for(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack, "act")
    stack.reply("/api/actions/downloads-pause", PAUSING)
    stack.reply("/api/actions/downloads-resume", PAUSING)
    await set_up(hass, entry)
    held = hass.states.get(PAUSED)
    assert held is not None
    assert held.state == STATE_UNKNOWN
    assert held.attributes[ATTR_ASSUMED_STATE] is True
    fired = async_capture_events(hass, JOB_EVENT)
    await hass.services.async_call("switch", "turn_on", {ATTR_ENTITY_ID: PAUSED}, blocking=True)
    assert state(hass, PAUSED) == STATE_ON
    await hass.services.async_call("switch", "turn_off", {ATTR_ENTITY_ID: PAUSED}, blocking=True)
    assert state(hass, PAUSED) == STATE_OFF
    assert [event.data["action"] for event in fired] == ["downloads-pause", "downloads-resume"]
    assert stack.asked("/api/actions/downloads-pause") == stack.asked("/api/actions/downloads-resume") == 1


async def test_a_refused_toggle_leaves_the_switch_as_it_was(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack, "act")
    stack.reply("/api/actions/downloads-pause", Reply(500, problem("FAIL-1", "The client is not answering.")))
    await set_up(hass, entry)
    with pytest.raises(HomeAssistantError):
        await hass.services.async_call("switch", "turn_on", {ATTR_ENTITY_ID: PAUSED}, blocking=True)
    assert state(hass, PAUSED) == STATE_UNKNOWN
