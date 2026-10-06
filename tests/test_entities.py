# Copyright (c) 2026 NightWorksIO
"""What each entity shows of what the stand-in's dashboard and doctor say, and what it shows where they cannot say."""

from typing import TYPE_CHECKING, Final

import pytest
from homeassistant.const import STATE_OFF, STATE_ON, STATE_UNKNOWN
from homeassistant.helpers import device_registry as dr

from custom_components.lemonfiber.const import DOMAIN, MANUFACTURER, MODEL
from tests.conftest import VERSION, dashboard, reading, ready, serve, transfer, unavailable, until
from tests.stack import Feed, event

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from pytest_homeassistant_custom_component.common import MockConfigEntry

    from tests.stack import Stack

PREFIX: Final = "127_0_0_1"


async def shown(hass: HomeAssistant, stack: Stack, entry: MockConfigEntry, **panels: object) -> None:
    """Set the entry up on a stream whose first dashboard has these panels, and wait for the doctor to be read."""
    feed = Feed()
    serve(stack, "read", feed)
    feed.queue.get_nowait()
    feed.say(event("dashboard", dashboard(**panels)))
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    await until(hass, lambda: entry.runtime_data.technical.diagnosis.data is not None)


def state(hass: HomeAssistant, platform: str, name: str) -> str:
    """Return the state of one of the stack's entities."""
    held = hass.states.get(f"{platform}.{PREFIX}_{name}")
    assert held is not None
    return held.state


def attributes(hass: HomeAssistant, platform: str, name: str) -> dict[str, object]:
    """Return the attributes of one of the stack's entities."""
    held = hass.states.get(f"{platform}.{PREFIX}_{name}")
    assert held is not None
    return dict(held.attributes)


async def test_a_healthy_stack_shows_its_figures(hass: HomeAssistant, stack: Stack, entry: MockConfigEntry) -> None:
    await shown(hass, stack, entry)
    assert state(hass, "sensor", "health") == "healthy"
    assert "worst" not in attributes(hass, "sensor", "health")
    assert state(hass, "sensor", "download_queue") == "5"
    assert state(hass, "sensor", "download_speed") == "2.0"
    assert attributes(hass, "sensor", "download_speed")["unit_of_measurement"] == "MB/s"
    assert state(hass, "sensor", "data_disk_free") == "500.0"
    assert state(hass, "binary_sensor", "needs_attention") == STATE_OFF
    assert state(hass, "binary_sensor", "vpn") == STATE_ON


async def test_the_findings_are_counted_by_severity_and_say_what_happened(
    hass: HomeAssistant, stack: Stack, entry: MockConfigEntry
) -> None:
    await shown(hass, stack, entry)
    assert state(hass, "sensor", "critical_findings") == "2"
    assert attributes(hass, "sensor", "critical_findings")["findings"] == [
        "The tunnel is down.",
        "Sonarr is not answering.",
    ]
    assert state(hass, "sensor", "warning_findings") == "1"
    assert state(hass, "sensor", "error_findings") == "0"
    assert state(hass, "sensor", "advisory_findings") == "0"
    assert attributes(hass, "sensor", "advisory_findings")["findings"] == []


async def test_a_stack_wanting_attention_names_the_worst_of_it(
    hass: HomeAssistant, stack: Stack, entry: MockConfigEntry
) -> None:
    health: dict[str, object] = {
        "affected": [],
        "standing": "critical",
        "wanting_attention": 2,
        "worst": "The disk is full.",
    }
    await shown(hass, stack, entry, health=health)
    assert state(hass, "sensor", "health") == "critical"
    assert attributes(hass, "sensor", "health")["worst"] == "The disk is full."
    assert state(hass, "binary_sensor", "needs_attention") == STATE_ON


async def test_a_stack_nothing_can_be_said_about_shows_unknown(
    hass: HomeAssistant, stack: Stack, entry: MockConfigEntry
) -> None:
    await shown(hass, stack, entry, health={"affected": [], "standing": "unknown", "wanting_attention": 0})
    assert state(hass, "sensor", "health") == STATE_UNKNOWN
    assert state(hass, "binary_sensor", "needs_attention") == STATE_UNKNOWN


@pytest.mark.parametrize(
    ("panels", "name"),
    [
        ({"queue": unavailable()}, "download_queue"),
        ({"transfers": unavailable()}, "download_speed"),
        ({"transfers": ready([transfer(reading(1)), transfer(reading(2, "stale"))])}, "download_speed"),
        ({"transfers": ready([transfer(reading(None, "unknown"))])}, "download_speed"),
        ({"storage": unavailable()}, "data_disk_free"),
        ({"storage": ready({"free": reading(7, "stale"), "hardlink": "linking"})}, "data_disk_free"),
    ],
)
async def test_a_figure_the_stack_cannot_give_now_is_unknown_rather_than_shown(
    hass: HomeAssistant, stack: Stack, entry: MockConfigEntry, panels: dict[str, object], name: str
) -> None:
    await shown(hass, stack, entry, **panels)
    assert state(hass, "sensor", name) == STATE_UNKNOWN


async def test_no_download_at_all_is_a_speed_of_zero(hass: HomeAssistant, stack: Stack, entry: MockConfigEntry) -> None:
    await shown(hass, stack, entry, transfers=ready([]))
    assert state(hass, "sensor", "download_speed") == "0.0"


async def test_traffic_outside_the_tunnel_is_a_vpn_that_is_not_up(
    hass: HomeAssistant, stack: Stack, entry: MockConfigEntry
) -> None:
    await shown(hass, stack, entry, vpn=ready({"country": "NL", "egress_matches": False, "exit_ip": "203.0.113.7"}))
    assert state(hass, "binary_sensor", "vpn") == STATE_OFF


async def test_a_tunnel_that_cannot_be_read_is_unknown(
    hass: HomeAssistant, stack: Stack, entry: MockConfigEntry
) -> None:
    await shown(hass, stack, entry, vpn=unavailable())
    assert state(hass, "binary_sensor", "vpn") == STATE_UNKNOWN


async def test_a_stack_without_a_vpn_has_no_vpn_entity(
    hass: HomeAssistant, stack: Stack, entry: MockConfigEntry
) -> None:
    await shown(hass, stack, entry, vpn=None)
    assert hass.states.get(f"binary_sensor.{PREFIX}_vpn") is None


async def test_the_stack_is_one_device_named_by_its_entry(
    hass: HomeAssistant, stack: Stack, entry: MockConfigEntry
) -> None:
    await shown(hass, stack, entry)
    [device] = dr.async_entries_for_config_entry(dr.async_get(hass), entry.entry_id)
    assert device.identifiers == {(DOMAIN, entry.entry_id)}
    assert (device.name, device.manufacturer, device.model, device.sw_version) == (
        "127.0.0.1",
        MANUFACTURER,
        MODEL,
        VERSION,
    )
    assert device.configuration_url == stack.url
