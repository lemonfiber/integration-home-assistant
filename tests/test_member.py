# Copyright (c) 2026 NightWorksIO
"""A member's own side, from the stream the stand-in opens for their key: their requests by state and what they are playing."""

from typing import TYPE_CHECKING, Final

from homeassistant.components.media_player.const import (
    ATTR_MEDIA_CONTENT_TYPE,
    ATTR_MEDIA_EPISODE,
    ATTR_MEDIA_SEASON,
    ATTR_MEDIA_SERIES_TITLE,
    ATTR_MEDIA_TITLE,
    MediaType,
)
from homeassistant.const import STATE_IDLE, STATE_PAUSED, STATE_PLAYING, STATE_UNAVAILABLE
from homeassistant.helpers import entity_registry as er

from tests.conftest import enabled, household, playback, playing, request, serve, until
from tests.stack import Feed, event

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from pytest_homeassistant_custom_component.common import MockConfigEntry

    from tests.stack import Stack

WAITING: Final = "sensor.127_0_0_1_requests_waiting_for_approval"
ON_THEIR_WAY: Final = "sensor.127_0_0_1_requests_on_their_way"
HERE: Final = "sensor.127_0_0_1_requests_here"
DECLINED: Final = "sensor.127_0_0_1_requests_declined"
GONE: Final = "sensor.127_0_0_1_requests_gone"
PLAYER: Final = "media_player.127_0_0_1_playing"


def state(hass: HomeAssistant, entity_id: str) -> str:
    """Return an entity's state."""
    held = hass.states.get(entity_id)
    assert held is not None
    return held.state


def attributes(hass: HomeAssistant, entity_id: str) -> dict[str, object]:
    """Return an entity's attributes."""
    held = hass.states.get(entity_id)
    assert held is not None
    return dict(held.attributes)


async def set_up(hass: HomeAssistant, entry: MockConfigEntry) -> None:
    """Set the entry up and let everything it started settle."""
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()


async def test_their_requests_are_counted_by_state_and_named_where_they_have_a_title(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack, "member")
    await set_up(hass, entry)
    assert (state(hass, WAITING), state(hass, ON_THEIR_WAY), state(hass, HERE), state(hass, DECLINED)) == (
        "1",
        "2",
        "1",
        "0",
    )
    assert attributes(hass, WAITING)["titles"] == []
    assert attributes(hass, ON_THEIR_WAY)["titles"] == ["Dune: Part Two", "Severance"]
    assert attributes(hass, HERE)["titles"] == ["Paddington in Peru"]


async def test_requests_gone_are_counted_by_an_entity_left_off_until_enabled(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack, "member")
    await set_up(hass, entry)
    assert hass.states.get(GONE) is None
    held = er.async_get(hass).async_get(GONE)
    assert held is not None
    assert held.disabled_by is er.RegistryEntryDisabler.INTEGRATION


async def test_requests_follow_what_the_stream_says_of_their_row(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    feed = serve(stack, "member")
    enabled(hass, entry, GONE, "requests_gone")
    await set_up(hass, entry)
    feed.say(event("household", household(request("here", "Dune: Part Two"), request("gone", "Severance"))))
    await until(hass, lambda: state(hass, HERE) == "1" and state(hass, ON_THEIR_WAY) == "0")
    assert attributes(hass, HERE)["titles"] == ["Dune: Part Two"]
    assert state(hass, GONE) == "1"


async def test_a_row_that_could_not_be_read_leaves_the_requests_unavailable(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    feed = serve(stack, "member")
    await set_up(hass, entry)
    feed.say(event("household", household(available=False)))
    await until(hass, lambda: state(hass, HERE) == STATE_UNAVAILABLE)
    assert state(hass, PLAYER) == STATE_IDLE


async def test_what_they_are_playing_is_shown_without_a_control(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    feed = serve(stack, "member")
    await set_up(hass, entry)
    assert state(hass, PLAYER) == STATE_IDLE
    assert attributes(hass, PLAYER)["supported_features"] == 0
    feed.say(event("playing", playing(playback())))
    await until(hass, lambda: state(hass, PLAYER) == STATE_PLAYING)
    shown = attributes(hass, PLAYER)
    assert shown[ATTR_MEDIA_TITLE] == "Who Is Alive?"
    assert shown[ATTR_MEDIA_SERIES_TITLE] == "Severance"
    assert (shown[ATTR_MEDIA_SEASON], shown[ATTR_MEDIA_EPISODE]) == ("2", "3")
    assert shown[ATTR_MEDIA_CONTENT_TYPE] == MediaType.EPISODE
    assert shown["device"] == "Living room TV"
    feed.say(event("playing", playing(playback(paused=True))))
    await until(hass, lambda: state(hass, PLAYER) == STATE_PAUSED)


async def test_a_film_is_named_as_one_and_has_no_season(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    feed = serve(stack, "member")
    await set_up(hass, entry)
    film: dict[str, object] = {
        "device": "Phone",
        "medium": "film",
        "member": "Ana",
        "member_id": "a1",
        "paused": False,
        "title": "Dune",
    }
    other = film | {"medium": "other", "title": "A home video"}
    feed.say(event("playing", playing(film, other)))
    await until(hass, lambda: state(hass, PLAYER) == STATE_PLAYING)
    shown = attributes(hass, PLAYER)
    assert shown[ATTR_MEDIA_TITLE] == "Dune"
    assert shown[ATTR_MEDIA_CONTENT_TYPE] == MediaType.MOVIE
    assert ATTR_MEDIA_SEASON not in shown
    assert ATTR_MEDIA_SERIES_TITLE not in shown
    feed.say(event("playing", playing(other)))
    await until(hass, lambda: attributes(hass, PLAYER).get(ATTR_MEDIA_TITLE) == "A home video")
    assert ATTR_MEDIA_CONTENT_TYPE not in attributes(hass, PLAYER)


async def test_a_media_server_that_could_not_say_leaves_the_player_unavailable(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    feed = serve(stack, "member")
    await set_up(hass, entry)
    feed.say(event("playing", playing(available=False)))
    await until(hass, lambda: state(hass, PLAYER) == STATE_UNAVAILABLE)
    assert state(hass, HERE) == "1"


async def test_after_a_gap_each_is_unavailable_until_the_stream_says_it_again(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    first, second = Feed(), Feed()
    serve(stack, "member", first, second)
    await set_up(hass, entry)
    first.say(event("playing", playing(playback()), "3"))
    await until(hass, lambda: state(hass, PLAYER) == STATE_PLAYING)
    first.end()
    await until(hass, lambda: state(hass, PLAYER) == state(hass, HERE) == STATE_UNAVAILABLE)
    second.say(event("household", household(request("here", "Dune: Part Two")), "4"))
    await until(hass, lambda: state(hass, HERE) == "1")
    assert state(hass, PLAYER) == STATE_UNAVAILABLE
    second.say(event("playing", playing(), "5"))
    await until(hass, lambda: state(hass, PLAYER) == STATE_IDLE)


async def test_kinds_a_member_entity_is_not_built_from_pass_by(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    feed = serve(stack, "member")
    await set_up(hass, entry)
    feed.say(
        event("held", {"holdings": []}),
        event("a-kind-from-a-later-stack", {}),
        event("household", household()),
    )
    await until(hass, lambda: state(hass, HERE) == "0")
