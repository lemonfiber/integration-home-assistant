# Copyright (c) 2026 NightWorksIO
"""lemonfiber in Home Assistant: a stack followed through an integration key.

The stack is reached only through the vendored sdk-python, whose own imports name
it `lemonfiber`, so its directory is put on the import path before anything here
imports it.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "_vendor"))

from typing import TYPE_CHECKING, Final

from homeassistant.const import CONF_API_KEY, CONF_URL, Platform
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady

from .connection import NotConnectedError, Reason, connect
from .const import CONF_PIN, DOMAIN
from .coordinator import StreamCoordinator, first_snapshot
from .runtime import LemonfiberConfigEntry, Runtime, Technical

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .connection import Connected

PLATFORMS: Final = [Platform.BINARY_SENSOR, Platform.SENSOR]


def not_set_up(refusal: NotConnectedError) -> ConfigEntryAuthFailed | ConfigEntryNotReady:
    """Return what Home Assistant is told when setup could not reach the stack: a new key, or another try."""
    kind = ConfigEntryAuthFailed if refusal.reason is Reason.KEY_REFUSED else ConfigEntryNotReady
    return kind(
        translation_domain=DOMAIN,
        translation_key=refusal.reason.value,
        translation_placeholders=dict(refusal.placeholders),
    )


async def async_setup_entry(hass: HomeAssistant, entry: LemonfiberConfigEntry) -> bool:
    """Reach the stack, learn the key's scope, and follow the stream where the scope reaches it."""
    try:
        connected = await connect(hass, entry.data[CONF_URL], entry.data[CONF_API_KEY], entry.data[CONF_PIN])
        technical = await set_up_technical(hass, entry, connected) if connected.technical else None
    except NotConnectedError as refusal:
        raise not_set_up(refusal) from refusal
    entry.runtime_data = Runtime(connected, technical)
    if technical is not None:
        entry.async_create_background_task(hass, technical.stream.follow(), f"{DOMAIN} stream")
        entry.async_create_background_task(hass, technical.diagnosis.async_refresh(), f"{DOMAIN} diagnosis")
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def set_up_technical(hass: HomeAssistant, entry: LemonfiberConfigEntry, connected: Connected) -> Technical:
    """Open the stream and wait for its first dashboard, so the entities are built from what the stack has."""
    version = await connected.version()
    stream = connected.client.events()
    stream_coordinator = StreamCoordinator(hass, entry, connected, stream, await first_snapshot(stream))
    return Technical(version, stream_coordinator, stream_coordinator.diagnosis)


async def async_unload_entry(hass: HomeAssistant, entry: LemonfiberConfigEntry) -> bool:
    """Let the entities go; the stream and the diagnosis stop with the entry's background tasks."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
