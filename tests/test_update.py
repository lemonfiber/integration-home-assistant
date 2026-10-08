# Copyright (c) 2026 NightWorksIO
"""Where each service stands against the tag this build pins, as the stand-in's reads say."""

from datetime import timedelta
from typing import TYPE_CHECKING, Final

import pytest
from homeassistant.components.update.const import (
    ATTR_INSTALLED_VERSION,
    ATTR_LATEST_VERSION,
    ATTR_RELEASE_SUMMARY,
    ATTR_TITLE,
    UpdateEntityFeature,
)
from homeassistant.const import (
    ATTR_ENTITY_ID,
    ATTR_SUPPORTED_FEATURES,
    STATE_OFF,
    STATE_ON,
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
)
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import entity_registry as er
from homeassistant.util import dt as dt_util
from pytest_homeassistant_custom_component.common import async_fire_time_changed

from tests.conftest import (
    SONARR_STEP,
    VERSION,
    dashboard,
    enabled,
    reauthenticating,
    serve,
    unavailable,
    until,
    update,
)
from tests.stack import Feed, Reply, envelope, event, problem

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from pytest_homeassistant_custom_component.common import MockConfigEntry
    from pytest_homeassistant_custom_component.typing import WebSocketGenerator

    from tests.stack import Stack

SONARR: Final = "update.127_0_0_1_update_of_sonarr"
RADARR: Final = "update.127_0_0_1_update_of_radarr"
JELLYFIN: Final = "update.127_0_0_1_update_of_jellyfin"
STACK: Final = "update.127_0_0_1_stack_update"
UPDATED: Final = Reply(202, envelope("job", {"action": "update", "job": "j-3"}))


async def set_up(hass: HomeAssistant, entry: MockConfigEntry) -> None:
    """Set the entry up, each service's update entity enabled, and wait for the versions to have been asked for."""
    for entity_id, service in ((SONARR, "sonarr"), (RADARR, "radarr"), (JELLYFIN, "jellyfin")):
        enabled(hass, entry, entity_id, f"update_{service}")
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
    assert hass.states.async_entity_ids("update") == [STACK]


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


def features(hass: HomeAssistant, entity_id: str) -> UpdateEntityFeature:
    """Return what an update entity offers."""
    held = hass.states.get(entity_id)
    assert held is not None
    return UpdateEntityFeature(held.attributes[ATTR_SUPPORTED_FEATURES])


async def install(hass: HomeAssistant, entity_id: str) -> None:
    """Ask an update entity to install."""
    await hass.services.async_call("update", "install", {ATTR_ENTITY_ID: entity_id}, blocking=True)


async def test_a_read_key_is_shown_updates_without_installing_them(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack)
    await set_up(hass, entry)
    assert UpdateEntityFeature.INSTALL not in features(hass, SONARR)
    assert UpdateEntityFeature.INSTALL not in features(hass, STACK)
    held = hass.states.get(SONARR)
    assert held is not None
    assert (
        held.attributes[ATTR_RELEASE_SUMMARY]
        == "A patch release: fixes, nothing that changes how it is set up."
    )


async def test_installing_a_service_agrees_to_its_step_and_reads_the_versions_again(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack, "act")
    stack.reply("/api/actions/update", UPDATED)
    stack.reply("/api/jobs/j-3", Reply(body=envelope("update", {"rehearsed": False})))
    await set_up(hass, entry)
    assert UpdateEntityFeature.INSTALL in features(hass, SONARR)
    assert UpdateEntityFeature.INSTALL not in features(hass, RADARR)
    await install(hass, SONARR)
    assert stack.bodies == [("/api/actions/update", {"service": "sonarr", "confirm": True})]
    await until(hass, lambda: stack.asked("/api/provenance") == 2)


async def test_a_step_the_stack_refuses_is_offered_as_no_install(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack, "act")
    stack.reply("/api/update", Reply(body=update(SONARR_STEP | {"refused": True})))
    await set_up(hass, entry)
    assert state(hass, SONARR) == STATE_ON
    assert UpdateEntityFeature.INSTALL not in features(hass, SONARR)
    assert UpdateEntityFeature.INSTALL not in features(hass, STACK)


async def test_a_refused_install_is_said_and_the_versions_read_again(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack, "act")
    stack.reply("/api/actions/update", Reply(409, problem("BUSY-1", "A restart is running.")))
    await set_up(hass, entry)
    with pytest.raises(HomeAssistantError):
        await install(hass, SONARR)
    await until(hass, lambda: stack.asked("/api/provenance") == 2)


async def test_the_stack_names_every_service_that_would_move(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack, "act")
    radarr = SONARR_STEP | {"service": "radarr", "current": "5.26.1", "target": "5.26.2", "refused": True}
    stack.reply("/api/update", Reply(body=update(SONARR_STEP, radarr)))
    await set_up(hass, entry)
    held = hass.states.get(STACK)
    assert held is not None
    assert held.state == STATE_ON
    assert (held.attributes[ATTR_INSTALLED_VERSION], held.attributes[ATTR_LATEST_VERSION]) == (
        "radarr 5.26.1, sonarr 4.0.14",
        "radarr 5.26.2, sonarr 4.0.15",
    )
    assert UpdateEntityFeature.INSTALL in features(hass, STACK)
    assert UpdateEntityFeature.INSTALL not in features(hass, RADARR)


async def test_the_stacks_notes_say_what_each_step_means(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
    hass_ws_client: WebSocketGenerator,
) -> None:
    serve(stack)
    await set_up(hass, entry)
    client = await hass_ws_client(hass)
    await client.send_json_auto_id({"type": "update/release_notes", "entity_id": STACK})
    answer = await client.receive_json()
    assert answer["result"] == (
        "- **sonarr** 4.0.14 → 4.0.15: A patch release: fixes, nothing that changes how it is set up."
    )
    await client.send_json_auto_id({"type": "update/release_notes", "entity_id": SONARR})
    assert (await client.receive_json())["success"] is False


async def test_a_stack_on_every_pin_stands_on_its_build(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
    hass_ws_client: WebSocketGenerator,
) -> None:
    serve(stack)
    stack.reply("/api/update", Reply(body=update()))
    await set_up(hass, entry)
    held = hass.states.get(STACK)
    assert held is not None
    assert held.state == STATE_OFF
    assert held.attributes[ATTR_INSTALLED_VERSION] == held.attributes[ATTR_LATEST_VERSION] == VERSION
    client = await hass_ws_client(hass)
    await client.send_json_auto_id({"type": "update/release_notes", "entity_id": STACK})
    assert (await client.receive_json())["result"] is None


async def test_installing_the_stack_names_no_service(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack, "act")
    stack.reply("/api/actions/update", UPDATED)
    stack.reply("/api/jobs/j-3", Reply(body=envelope("update", {"rehearsed": False})))
    await set_up(hass, entry)
    await install(hass, STACK)
    assert stack.bodies == [("/api/actions/update", {"confirm": True})]
    await until(hass, lambda: stack.asked("/api/provenance") == 2)


async def test_each_services_update_is_left_off_until_enabled(
    hass: HomeAssistant,
    stack: Stack,
    entry: MockConfigEntry,
) -> None:
    serve(stack)
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    assert hass.states.async_entity_ids("update") == [STACK]
    held = er.async_get(hass).async_get(SONARR)
    assert held is not None
    assert held.disabled_by is er.RegistryEntryDisabler.INTEGRATION
