# Copyright (c) 2026 NightWorksIO
"""The controls an `act` key gets: running the doctor, and restarting and pausing or resuming downloads, rehearsed first."""

from typing import TYPE_CHECKING, Final, cast

import pytest
from homeassistant.const import (
    ATTR_ASSUMED_STATE,
    ATTR_ENTITY_ID,
    STATE_OFF,
    STATE_ON,
    STATE_UNKNOWN,
    EntityCategory,
)
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import entity_registry as er
from pytest_homeassistant_custom_component.common import async_capture_events

from custom_components.lemonfiber.connection import Reason
from custom_components.lemonfiber.jobs import JOB_EVENT
from tests.conftest import (
    DIAGNOSIS,
    capabilities,
    dashboard,
    downloader,
    enabled,
    ready,
    reauthenticating,
    serve,
    unavailable,
    until,
)
from tests.stack import Reply, envelope, event, problem

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from pytest_homeassistant_custom_component.common import MockConfigEntry

    from tests.stack import Stack

DOCTOR: Final = "button.127_0_0_1_run_the_doctor"
PAUSED: Final = "switch.127_0_0_1_downloads_paused"
RESTART_STACK: Final = "button.127_0_0_1_restart_the_stack"
RESTART_SONARR: Final = "button.127_0_0_1_restart_sonarr"
RESTARTED: Final = Reply(202, envelope("job", {"action": "restart", "job": "j-2"}))
STARTED: Final = Reply(202, envelope("job", {"action": "diagnose", "job": "j-1"}))
RESTART_OFFER: Final = Reply(body=envelope("lifecycle", {"offer": "o-restart", "rehearsed": True}))
PAUSE_OFFER: Final = Reply(
    body=envelope("pausing", {"asked": "pause", "clients": [], "offer": "o-pause", "rehearsed": True}),
)
PAUSING: Final = Reply(
    body=envelope("pausing", {"asked": "pause", "clients": [], "offer": "o-pause", "rehearsed": False}),
)


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
    assert hass.states.async_entity_ids("button") == []


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
    states["/api/actions/restart"] = "unconfigured"
    stack.reply("/api/capabilities", Reply(body=switched_off))
    await set_up(hass, entry)
    assert hass.states.get(DOCTOR) is hass.states.get(PAUSED) is None
    assert hass.states.async_entity_ids("button") == []


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


async def test_the_downloads_switch_shows_what_the_clients_say(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    feed = serve(stack, "act")
    await set_up(hass, entry)
    held = hass.states.get(PAUSED)
    assert held is not None
    assert held.state == STATE_OFF
    assert ATTR_ASSUMED_STATE not in held.attributes
    clients = ready([downloader("qbittorrent", "paused"), downloader("sabnzbd", "unknown")])
    feed.say(event("dashboard", dashboard(downloaders=clients)))
    await until(hass, lambda: state(hass, PAUSED) == STATE_ON)
    mixed = ready([downloader("qbittorrent", "paused"), downloader("sabnzbd", "fetching")])
    feed.say(event("dashboard", dashboard(downloaders=mixed)))
    await until(hass, lambda: state(hass, PAUSED) == STATE_OFF)
    feed.say(event("dashboard", dashboard(downloaders=ready([downloader("qbittorrent", "unknown")]))))
    await until(hass, lambda: state(hass, PAUSED) == STATE_UNKNOWN)
    feed.say(event("dashboard", dashboard(downloaders=unavailable())))
    await hass.async_block_till_done()
    assert state(hass, PAUSED) == STATE_UNKNOWN


async def test_toggling_rehearses_then_asks_with_the_offer_and_waits_for_the_clients_to_say_so(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack, "act")
    stack.reply("/api/actions/downloads-pause", PAUSE_OFFER, PAUSING)
    stack.reply("/api/actions/downloads-resume", PAUSE_OFFER, PAUSING)
    await set_up(hass, entry)
    fired = async_capture_events(hass, JOB_EVENT)
    await hass.services.async_call("switch", "turn_on", {ATTR_ENTITY_ID: PAUSED}, blocking=True)
    assert state(hass, PAUSED) == STATE_OFF
    await hass.services.async_call("switch", "turn_off", {ATTR_ENTITY_ID: PAUSED}, blocking=True)
    assert [event.data["action"] for event in fired] == ["downloads-pause", "downloads-resume"]
    assert stack.bodies == [
        ("/api/actions/downloads-pause", {"dry_run": True}),
        ("/api/actions/downloads-pause", {"offer": "o-pause"}),
        ("/api/actions/downloads-resume", {"dry_run": True}),
        ("/api/actions/downloads-resume", {"offer": "o-pause"}),
    ]


async def test_a_refused_toggle_leaves_the_switch_as_the_clients_say(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack, "act")
    stack.reply("/api/actions/downloads-pause", Reply(500, problem("FAIL-1", "The client is not answering.")))
    await set_up(hass, entry)
    with pytest.raises(HomeAssistantError):
        await hass.services.async_call("switch", "turn_on", {ATTR_ENTITY_ID: PAUSED}, blocking=True)
    assert state(hass, PAUSED) == STATE_OFF
    assert stack.asked("/api/actions/downloads-pause") == 1


async def test_a_call_whose_offer_has_moved_is_refused_in_the_stacks_words(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack, "act")
    moved = Reply(409, problem("RATE-6", "A client changed since this was offered."))
    stack.reply("/api/actions/downloads-pause", PAUSE_OFFER, moved)
    await set_up(hass, entry)
    fired = async_capture_events(hass, JOB_EVENT)
    with pytest.raises(HomeAssistantError) as raised:
        await hass.services.async_call("switch", "turn_on", {ATTR_ENTITY_ID: PAUSED}, blocking=True)
    assert raised.value.translation_placeholders == {"sentence": "A client changed since this was offered."}
    assert fired[0].data["outcome"] == "failed"


async def test_a_service_is_restarted_alone_and_the_restart_followed(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack, "act")
    stack.reply("/api/actions/restart", RESTART_OFFER, RESTARTED)
    stack.reply("/api/jobs/j-2", Reply(body=envelope("lifecycle", {"rehearsed": False})))
    enabled(hass, entry, RESTART_SONARR, "restart_sonarr")
    await set_up(hass, entry)
    fired = async_capture_events(hass, JOB_EVENT)
    await hass.services.async_call("button", "press", {ATTR_ENTITY_ID: RESTART_SONARR}, blocking=True)
    assert stack.bodies == [
        ("/api/actions/restart", {"services": ["sonarr"], "dry_run": True}),
        ("/api/actions/restart", {"services": ["sonarr"], "offer": "o-restart"}),
    ]
    assert [event.data for event in fired] == [
        {"entry_id": entry.entry_id, "action": "restart", "job": "j-2", "outcome": "finished"},
    ]


async def test_the_whole_stack_is_restarted_by_naming_no_service(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack, "act")
    stack.reply("/api/actions/restart", RESTART_OFFER, RESTARTED)
    stack.reply("/api/jobs/j-2", Reply(body=envelope("lifecycle", {"rehearsed": False})))
    await set_up(hass, entry)
    await hass.services.async_call("button", "press", {ATTR_ENTITY_ID: RESTART_STACK}, blocking=True)
    assert stack.bodies == [
        ("/api/actions/restart", {"dry_run": True}),
        ("/api/actions/restart", {"offer": "o-restart"}),
    ]


async def test_a_rehearsal_naming_no_offer_is_followed_by_the_call_as_it_was(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack, "act")
    stack.reply("/api/actions/restart", Reply(body=envelope("lifecycle", {"rehearsed": True})), RESTARTED)
    stack.reply("/api/jobs/j-2", Reply(body=envelope("lifecycle", {"rehearsed": False})))
    await set_up(hass, entry)
    await hass.services.async_call("button", "press", {ATTR_ENTITY_ID: RESTART_STACK}, blocking=True)
    assert stack.bodies == [("/api/actions/restart", {"dry_run": True}), ("/api/actions/restart", {})]


async def test_the_doctor_is_run_without_a_rehearsal(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack, "act")
    stack.reply("/api/actions/diagnose", Reply(body=DIAGNOSIS))
    await set_up(hass, entry)
    await press(hass)
    assert stack.bodies == [("/api/actions/diagnose", {})]


async def test_a_refused_restart_is_said_in_the_stacks_words(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack, "act")
    stack.reply("/api/actions/restart", Reply(409, problem("BUSY-1", "An update is running.")))
    enabled(hass, entry, RESTART_SONARR, "restart_sonarr")
    await set_up(hass, entry)
    with pytest.raises(HomeAssistantError) as raised:
        await hass.services.async_call("button", "press", {ATTR_ENTITY_ID: RESTART_SONARR}, blocking=True)
    assert raised.value.translation_placeholders == {"sentence": "An update is running."}


async def test_the_stack_restart_is_on_and_each_services_left_off_until_enabled(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack, "act")
    await set_up(hass, entry)
    assert hass.states.get(RESTART_STACK) is not None
    assert hass.states.get(RESTART_SONARR) is None
    registry = er.async_get(hass)
    for entity_id in (RESTART_STACK, RESTART_SONARR):
        held = registry.async_get(entity_id)
        assert held is not None
        assert held.entity_category is EntityCategory.CONFIG
