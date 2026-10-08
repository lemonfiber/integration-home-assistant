# Copyright (c) 2026 NightWorksIO
"""Each alert the stand-in's stream carries, fired as an event at its onset and at its resolution."""

from typing import TYPE_CHECKING, Final

from homeassistant.components.event import ATTR_EVENT_TYPE, ATTR_EVENT_TYPES
from homeassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN
from pytest_homeassistant_custom_component.common import async_capture_events

from custom_components.lemonfiber.alerts import ALERT_EVENT
from tests.conftest import KEY, dashboard, serve, until
from tests.stack import Feed, event

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from pytest_homeassistant_custom_component.common import MockConfigEntry

    from tests.stack import Stack

ALERTS: Final = "event.127_0_0_1_alerts"


def state_of(hass: HomeAssistant) -> str:
    """Return the alerts entity's state."""
    held = hass.states.get(ALERTS)
    assert held is not None
    return held.state


def attribute(hass: HomeAssistant, name: str) -> object:
    """Return one attribute of the alerts entity."""
    held = hass.states.get(ALERTS)
    assert held is not None
    return held.attributes.get(name)


def alert(moment: str, **more: object) -> dict[str, object]:
    """Return an alert as the stack says one: the tunnel dropping, or coming back."""
    return {
        "affected": ["vpn.tunnel", "vpn.egress"],
        "check": "vpn.tunnel",
        "kind": "vpn-down",
        "meaning": "Downloads are held until the tunnel is back, so nothing leaves outside it.",
        "moment": moment,
        "remedies": ["Restart the VPN gateway.", "Check the provider's status page."],
        "severity": "critical",
        "summary": "The VPN tunnel dropped.",
        **more,
    }


ONSET: Final = alert("onset", id="vpn.tunnel#3", exit=1)
RESOLVED: Final = alert("resolved", id="vpn.tunnel#3")


async def test_an_alert_is_fired_at_onset_and_at_resolution_with_what_to_do(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    feed = serve(stack)
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    fired = async_capture_events(hass, ALERT_EVENT)
    feed.say(event("alert", ONSET, "2"), event("alert", RESOLVED, "3"))
    await until(hass, lambda: len(fired) == 2)
    onset, resolved = (one.data for one in fired)
    assert onset == {
        "entry_id": entry.entry_id,
        "id": "vpn.tunnel#3",
        "moment": "onset",
        "severity": "critical",
        "kind": "vpn-down",
        "check": "vpn.tunnel",
        "affected": ["vpn.tunnel", "vpn.egress"],
        "summary": "The VPN tunnel dropped.",
        "meaning": "Downloads are held until the tunnel is back, so nothing leaves outside it.",
        "remedies": ["Restart the VPN gateway.", "Check the provider's status page."],
        "exit": 1,
    }
    assert resolved["moment"] == "resolved"
    assert resolved["id"] == onset["id"]
    assert "exit" not in resolved


async def test_an_alert_names_nothing_the_entry_holds(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    feed = serve(stack)
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    fired = async_capture_events(hass, ALERT_EVENT)
    feed.say(event("alert", alert("onset")))
    await until(hass, lambda: len(fired) == 1)
    carried = repr(fired[0].data)
    for held in (KEY, stack.url, stack.pin, "127.0.0.1"):
        assert held not in carried
    assert "id" not in fired[0].data


async def test_an_alert_held_from_before_a_gap_is_not_fired_again(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    first, second = Feed(), Feed()
    serve(stack, "read", first, second)
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    fired = async_capture_events(hass, ALERT_EVENT)
    first.say(event("alert", ONSET, "2"))
    await until(hass, lambda: len(fired) == 1)
    first.end()
    second.say(event("dashboard", dashboard(), "4"), event("alert", RESOLVED, "5"))
    await until(hass, lambda: len(fired) == 2)
    assert [one.data["moment"] for one in fired] == ["onset", "resolved"]


async def test_the_alerts_entity_shows_the_last_alert_and_which_way_it_went(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    feed = serve(stack)
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    held = hass.states.get(ALERTS)
    assert held is not None
    assert held.state == STATE_UNKNOWN
    assert held.attributes[ATTR_EVENT_TYPES] == ["onset", "resolved"]
    feed.say(event("alert", ONSET, "2"))
    await until(hass, lambda: attribute(hass, ATTR_EVENT_TYPE) == "onset")
    shown = hass.states.get(ALERTS)
    assert shown is not None
    assert shown.attributes["summary"] == "The VPN tunnel dropped."
    assert shown.attributes["remedies"] == ["Restart the VPN gateway.", "Check the provider's status page."]
    assert "moment" not in shown.attributes
    feed.say(event("alert", RESOLVED, "3"))
    await until(hass, lambda: attribute(hass, ATTR_EVENT_TYPE) == "resolved")


async def test_the_alerts_entity_goes_unavailable_with_the_stream(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    first, second = Feed(), Feed()
    serve(stack, "read", first, second)
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    first.end()
    await until(hass, lambda: state_of(hass) == STATE_UNAVAILABLE)
    second.say(event("dashboard", dashboard(), "4"))
    await until(hass, lambda: state_of(hass) != STATE_UNAVAILABLE)
