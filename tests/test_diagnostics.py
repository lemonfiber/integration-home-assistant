# Copyright (c) 2026 NightWorksIO
"""What an entry hands over for a diagnosis, and that the key, the address and the pin are never in it."""

import json
from typing import TYPE_CHECKING, Any, cast

import pytest
from homeassistant.components.diagnostics import REDACTED

from custom_components.lemonfiber.diagnostics import async_get_config_entry_diagnostics
from tests.conftest import KEY, VERSION, serve, until

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from pytest_homeassistant_custom_component.common import MockConfigEntry

    from tests.stack import Stack


async def handed_over(hass: HomeAssistant, entry: MockConfigEntry) -> dict[str, Any]:
    """Set the entry up, wait for the doctor, and return what its diagnostics hand over."""
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    technical = entry.runtime_data.technical
    await until(hass, lambda: technical is None or technical.diagnosis.data is not None)
    return cast("dict[str, Any]", await async_get_config_entry_diagnostics(hass, entry))


@pytest.mark.parametrize("scope", ["read", "member"])
async def test_the_key_the_address_and_the_pin_appear_nowhere(
    hass: HomeAssistant, stack: Stack, entry: MockConfigEntry, scope: str
) -> None:
    serve(stack, scope)
    written = json.dumps(await handed_over(hass, entry), default=str)
    for secret in (KEY, stack.url, stack.pin, "127.0.0.1", str(stack.port)):
        assert secret not in written


async def test_what_the_stack_said_is_handed_over_with_its_scope_and_state(
    hass: HomeAssistant, stack: Stack, entry: MockConfigEntry
) -> None:
    serve(stack)
    said = await handed_over(hass, entry)
    assert said["scope"] == "read"
    assert said["state"] == "connected"
    assert said["version"] == VERSION
    assert said["capabilities"]["/api/checks"] == "available"
    dashboard = said["dashboard"]
    assert dashboard["door"] == dashboard["household"] == REDACTED
    assert dashboard["health"]["standing"] == "healthy"
    assert len(said["diagnosis"]["findings"]) == 5
    assert said["entry"]["data"] == {"url": REDACTED, "api_key": REDACTED, "pin": REDACTED}
    assert said["entry"]["title"] == said["entry"]["unique_id"] == REDACTED


async def test_a_members_entry_hands_over_nothing_technical(
    hass: HomeAssistant, stack: Stack, entry: MockConfigEntry
) -> None:
    serve(stack, "member")
    said = await handed_over(hass, entry)
    assert said["scope"] == "member"
    assert {"state", "version", "dashboard", "diagnosis"}.isdisjoint(said)
