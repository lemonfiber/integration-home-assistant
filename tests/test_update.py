# Copyright (c) 2026 NightWorksIO
"""Where each service stands against the tag this build pins, as the stand-in's reads say."""

from datetime import timedelta
from typing import TYPE_CHECKING, Final

from homeassistant.components.update.const import ATTR_INSTALLED_VERSION, ATTR_LATEST_VERSION, ATTR_TITLE
from homeassistant.const import STATE_OFF, STATE_ON, STATE_UNAVAILABLE, STATE_UNKNOWN
from homeassistant.util import dt as dt_util
from pytest_homeassistant_custom_component.common import async_fire_time_changed

from tests.conftest import dashboard, reauthenticating, serve, unavailable, until
from tests.stack import Feed, Reply, event, problem

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from pytest_homeassistant_custom_component.common import MockConfigEntry

    from tests.stack import Stack

SONARR: Final = "update.127_0_0_1_update_of_sonarr"
RADARR: Final = "update.127_0_0_1_update_of_radarr"
JELLYFIN: Final = "update.127_0_0_1_update_of_jellyfin"


async def set_up(hass: HomeAssistant, entry: MockConfigEntry) -> None:
    """Set the entry up and wait for the versions to have been asked for."""
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    await until(
        hass,
        lambda: (
            entry.runtime_data.technical.versions.data is not None
            or not entry.runtime_data.technical.versions.last_update_success
        ),
    )


def state(hass: HomeAssistant, entity_id: str) -> str:
    """Return an entity's state."""
    held = hass.states.get(entity_id)
    assert held is not None
    return held.state


async def test_a_service_off_its_pin_has_an_update(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack)
    await set_up(hass, entry)
    held = hass.states.get(SONARR)
    assert held is not None
    assert held.state == STATE_ON
    assert (held.attributes[ATTR_INSTALLED_VERSION], held.attributes[ATTR_LATEST_VERSION]) == (
        "4.0.14",
        "4.0.15",
    )
    assert held.attributes[ATTR_TITLE] == "Sonarr"
    assert ("/api/update", {"what": "stack"}) in stack.queries


async def test_a_service_on_its_pin_is_current(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack)
    await set_up(hass, entry)
    held = hass.states.get(RADARR)
    assert held is not None
    assert held.state == STATE_OFF
    assert held.attributes[ATTR_INSTALLED_VERSION] == held.attributes[ATTR_LATEST_VERSION] == "5.26.2"


async def test_a_service_the_stack_names_no_version_for_is_unknown(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack)
    await set_up(hass, entry)
    assert state(hass, JELLYFIN) == STATE_UNKNOWN


async def test_no_service_panel_means_no_update_entity(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    feed = Feed()
    serve(stack, "read", feed)
    feed.queue.get_nowait()
    feed.say(event("dashboard", dashboard(services=unavailable())))
    await set_up(hass, entry)
    assert hass.states.async_entity_ids("update") == []


async def test_versions_that_cannot_be_read_leave_the_entities_unavailable(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack)
    stack.reply("/api/update", Reply(500, problem("FAIL-1", "The engine is not answering.")))
    await set_up(hass, entry)
    assert state(hass, SONARR) == STATE_UNAVAILABLE


async def test_versions_refusing_the_key_ask_for_a_new_one(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack)
    stack.reply("/api/provenance", Reply(403, problem("ADMIT-4", "Not admitted.")))
    await set_up(hass, entry)
    await until(hass, lambda: reauthenticating(hass))


async def test_the_versions_are_read_again_every_hour(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack)
    await set_up(hass, entry)
    await until(hass, lambda: state(hass, SONARR) == STATE_ON)
    async_fire_time_changed(hass, dt_util.utcnow() + timedelta(hours=1, seconds=1))
    await until(hass, lambda: stack.asked("/api/provenance") == 2)
