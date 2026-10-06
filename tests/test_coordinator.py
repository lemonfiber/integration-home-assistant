# Copyright (c) 2026 NightWorksIO
"""Following the stand-in's stream: live values, gaps, a resumed stream, a refused key, a lost stack, and the doctor."""

from datetime import timedelta
from typing import TYPE_CHECKING, Final

from homeassistant.config_entries import ConfigEntryState
from homeassistant.const import STATE_ON, STATE_UNAVAILABLE
from homeassistant.util import dt as dt_util
from pytest_homeassistant_custom_component.common import async_fire_time_changed

from custom_components.lemonfiber.coordinator import State
from tests.conftest import capabilities, dashboard, reauthenticating, serve, until
from tests.stack import Feed, Reply, event, problem

if TYPE_CHECKING:
    import pytest
    from homeassistant.core import HomeAssistant
    from pytest_homeassistant_custom_component.common import MockConfigEntry

    from tests.stack import Stack

HEALTH: Final = "sensor.127_0_0_1_health"
QUEUE: Final = "sensor.127_0_0_1_download_queue"
CRITICAL: Final = "sensor.127_0_0_1_critical_findings"
SONARR: Final = "update.127_0_0_1_update_of_sonarr"


def state(hass: HomeAssistant, entity_id: str) -> str:
    """Return an entity's state."""
    held = hass.states.get(entity_id)
    assert held is not None
    return held.state


async def set_up(hass: HomeAssistant, entry: MockConfigEntry) -> None:
    """Set the entry up and let everything it started settle."""
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()


async def test_what_the_stream_carries_is_what_the_entities_show(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    feed = serve(stack)
    await set_up(hass, entry)
    assert state(hass, QUEUE) == "5"
    feed.say(
        event(
            "dashboard",
            dashboard(queue={"panel": "ready", "data": [{"service": "x", "depth": 9, "stuck": 0}]}),
        ),
    )
    await until(hass, lambda: state(hass, QUEUE) == "9")


async def test_kinds_the_entities_are_not_built_from_pass_by(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    feed = serve(stack)
    await set_up(hass, entry)
    feed.say(
        event("news", {"items": []}),
        event("a-kind-from-a-later-stack", {}),
        event("dashboard", dashboard(queue={"panel": "ready", "data": []})),
    )
    await until(hass, lambda: state(hass, QUEUE) == "0")
    assert entry.runtime_data.technical.stream.state is State.CONNECTED


async def test_a_gap_shows_every_stream_built_entity_unavailable_until_the_stream_says_it_again(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
    caplog: pytest.LogCaptureFixture,
) -> None:
    first, second = Feed(), Feed()
    serve(stack, "read", first, second)
    await set_up(hass, entry)
    stream = entry.runtime_data.technical.stream
    await until(hass, lambda: state(hass, CRITICAL) == "2" and state(hass, SONARR) == STATE_ON)
    first.end()
    await until(hass, lambda: state(hass, HEALTH) == STATE_UNAVAILABLE)
    assert stream.state is State.STALE
    assert state(hass, QUEUE) == STATE_UNAVAILABLE
    assert state(hass, CRITICAL) == STATE_UNAVAILABLE
    assert state(hass, SONARR) == STATE_UNAVAILABLE
    await until(hass, lambda: stack.asked("/api/events") == 2)
    second.say(event("dashboard", dashboard()))
    await until(hass, lambda: state(hass, HEALTH) == "healthy")
    assert stream.state is State.CONNECTED
    assert state(hass, CRITICAL) == "2"
    assert state(hass, SONARR) == STATE_ON
    await until(hass, lambda: stack.asked("/api/capabilities") == 2)
    assert entry.state is ConfigEntryState.LOADED
    assert stack.asked("/api/version") == 1
    said = [
        record.getMessage()
        for record in caplog.records
        if record.name == "custom_components.lemonfiber" and record.getMessage().startswith("The stream")
    ]
    assert said == [
        "The stream from 127.0.0.1 is stale; its entities are unavailable",
        "The stream from 127.0.0.1 resumed",
    ]


async def test_a_scope_that_changed_across_a_gap_reloads_the_entry(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    first, second, reloaded = Feed(), Feed(), Feed()
    serve(stack, "read", first, second, reloaded)
    reloaded.say(event("dashboard", dashboard()))
    await set_up(hass, entry)
    stack.reply("/api/capabilities", Reply(body=capabilities("act")))
    first.end()
    await until(hass, lambda: stack.asked("/api/events") == 2)
    second.say(event("dashboard", dashboard()))
    await until(hass, lambda: stack.asked("/api/version") == 2)
    await until(
        hass,
        lambda: entry.state is ConfigEntryState.LOADED and entry.runtime_data.connected.scope == "act",
    )


async def test_a_scope_that_cannot_be_read_again_leaves_the_entry_as_it_is(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    first, second = Feed(), Feed()
    serve(stack, "read", first, second)
    await set_up(hass, entry)
    stack.reply("/api/capabilities", Reply(500, problem("FAIL-1", "Busy.")))
    first.end()
    await until(hass, lambda: stack.asked("/api/events") == 2)
    second.say(event("dashboard", dashboard()))
    await until(hass, lambda: stack.asked("/api/capabilities") == 2)
    await hass.async_block_till_done()
    assert stack.asked("/api/version") == 1
    assert state(hass, HEALTH) == "healthy"


async def test_a_key_refused_when_the_stream_reopens_asks_for_a_new_one(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    first = Feed()
    serve(stack, "read", first)
    stack.stream(first, Reply(403, problem("ADMIT-4", "Not admitted.")))
    await set_up(hass, entry)
    first.end()
    await until(hass, lambda: entry.runtime_data.technical.stream.state is State.REFUSED)
    assert state(hass, HEALTH) == STATE_UNAVAILABLE
    assert reauthenticating(hass)


async def test_a_stream_that_cannot_be_reopened_hands_the_entry_back_to_be_set_up_again(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    first = Feed()
    serve(stack, "read", first)
    stack.stream(first, Reply(404, problem("GONE-2", "There is no stream here.")))
    await set_up(hass, entry)
    stream = entry.runtime_data.technical.stream
    first.end()
    await until(hass, lambda: entry.state is ConfigEntryState.SETUP_RETRY)
    assert stream.state is State.UNREACHABLE


async def test_the_health_moving_has_the_doctor_read_again(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    feed = serve(stack)
    await set_up(hass, entry)
    await until(hass, lambda: state(hass, CRITICAL) == "2")
    feed.say(event("dashboard", dashboard(queue={"panel": "ready", "data": []})))
    await until(hass, lambda: state(hass, QUEUE) == "0")
    assert stack.asked("/api/checks") == 1
    moved: dict[str, object] = {
        "affected": [],
        "standing": "degraded",
        "wanting_attention": 1,
        "worst": "The tunnel is down.",
    }
    feed.say(event("dashboard", dashboard(health=moved)))
    await until(hass, lambda: stack.asked("/api/checks") == 2)


async def test_the_doctor_is_read_again_every_hour(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack)
    await set_up(hass, entry)
    await until(hass, lambda: state(hass, CRITICAL) == "2")
    async_fire_time_changed(hass, dt_util.utcnow() + timedelta(hours=1, seconds=1))
    await until(hass, lambda: stack.asked("/api/checks") == 2)


async def test_a_doctor_that_cannot_be_read_leaves_its_findings_unavailable(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack)
    stack.reply("/api/checks", Reply(500, problem("FAIL-1", "The engine is not answering.")))
    await set_up(hass, entry)
    await until(hass, lambda: state(hass, CRITICAL) == STATE_UNAVAILABLE)
    assert state(hass, HEALTH) == "healthy"


async def test_a_doctor_refusing_the_key_asks_for_a_new_one(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack)
    stack.reply("/api/checks", Reply(403, problem("ADMIT-4", "Not admitted.")))
    await set_up(hass, entry)
    await until(
        hass,
        lambda: reauthenticating(hass),
    )
