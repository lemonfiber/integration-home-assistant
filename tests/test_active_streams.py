# Copyright (c) 2026 NightWorksIO
"""What the media server is playing, as the stand-in's stream says it to a `read` key."""

from typing import TYPE_CHECKING, Final

from homeassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN

from tests.conftest import dashboard, playback, playing, serve, until
from tests.stack import Feed, event

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from pytest_homeassistant_custom_component.common import MockConfigEntry

    from tests.stack import Stack

ACTIVE: Final = "sensor.127_0_0_1_active_streams"


def state(hass: HomeAssistant) -> str:
    """Return the sensor's state."""
    held = hass.states.get(ACTIVE)
    assert held is not None
    return held.state


def sessions(hass: HomeAssistant) -> object:
    """Return who the sensor says is watching what."""
    held = hass.states.get(ACTIVE)
    assert held is not None
    return held.attributes["sessions"]


async def set_up(hass: HomeAssistant, entry: MockConfigEntry) -> None:
    """Set the entry up and let everything it started settle."""
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()


async def test_it_is_unavailable_until_the_stream_says_what_is_playing(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    feed = serve(stack)
    await set_up(hass, entry)
    assert state(hass) == STATE_UNAVAILABLE
    feed.say(event("playing", playing()))
    await until(hass, lambda: state(hass) == "0")
    assert sessions(hass) == []


async def test_it_counts_the_sessions_and_says_who_is_watching_what(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    feed = serve(stack)
    await set_up(hass, entry)
    film: dict[str, object] = {
        "device": "Phone",
        "medium": "film",
        "member": "Bo",
        "member_id": "b2",
        "paused": True,
        "title": "Dune",
    }
    feed.say(event("playing", playing(playback(), film)))
    await until(hass, lambda: state(hass) == "2")
    assert sessions(hass) == [
        {
            "member": "Ana",
            "title": "Who Is Alive?",
            "device": "Living room TV",
            "paused": False,
            "series": "Severance",
            "season": 2,
            "episode": 3,
        },
        {"member": "Bo", "title": "Dune", "device": "Phone", "paused": True},
    ]


async def test_a_media_server_that_could_not_say_is_unknown(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    feed = serve(stack)
    await set_up(hass, entry)
    feed.say(event("playing", playing(playback(), available=False)))
    await until(hass, lambda: state(hass) == STATE_UNKNOWN)
    assert sessions(hass) == []


async def test_after_a_gap_it_is_unavailable_until_the_stream_says_it_again(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    first, second = Feed(), Feed()
    serve(stack, "read", first, second)
    await set_up(hass, entry)
    first.say(event("playing", playing(playback()), "2"))
    await until(hass, lambda: state(hass) == "1")
    first.end()
    await until(hass, lambda: state(hass) == STATE_UNAVAILABLE)
    second.say(event("dashboard", dashboard(), "3"))
    await until(hass, lambda: entry.runtime_data.technical.stream.last_update_success)
    assert state(hass) == STATE_UNAVAILABLE
    second.say(event("playing", playing(), "4"))
    await until(hass, lambda: state(hass) == "0")
