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
from homeassistant.helpers import issue_registry as ir

from .connection import NotConnectedError, Reason, connect
from .const import CONF_PIN, DOMAIN
from .coordinator import StreamCoordinator, VersionsCoordinator, first_snapshot
from .runtime import LemonfiberConfigEntry, Runtime, Technical

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .connection import Connected

REPAIRABLE: Final = frozenset({Reason.PIN_MISMATCH, Reason.NOT_LEMONFIBER, Reason.VERSION_MISMATCH})
"""What only the person can put right, and so is raised as a repair until setup next reaches the stack."""

PLATFORMS: Final = [
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.EVENT,
    Platform.SENSOR,
    Platform.SWITCH,
    Platform.UPDATE,
]


def not_set_up(refusal: NotConnectedError) -> ConfigEntryAuthFailed | ConfigEntryNotReady:
    """Return what Home Assistant is told when setup could not reach the stack: a new key, or another try."""
    kind = ConfigEntryAuthFailed if refusal.reason is Reason.KEY_REFUSED else ConfigEntryNotReady
    return kind(
        translation_domain=DOMAIN,
        translation_key=refusal.reason.value,
        translation_placeholders=dict(refusal.placeholders),
    )


def issue_of(entry: LemonfiberConfigEntry, reason: Reason) -> str:
    """Return the repair an entry raises for a reason, one per entry and reason."""
    return f"{entry.entry_id}_{reason}"


async def async_setup_entry(hass: HomeAssistant, entry: LemonfiberConfigEntry) -> bool:
    """Reach the stack, learn the key's scope, and follow the stream where the scope reaches it."""
    try:
        connected = await connect(hass, entry.data[CONF_URL], entry.data[CONF_API_KEY], entry.data[CONF_PIN])
        technical = await set_up_technical(hass, entry, connected) if connected.technical else None
    except NotConnectedError as refusal:
        if refusal.reason in REPAIRABLE:
            ir.async_create_issue(
                hass,
                DOMAIN,
                issue_of(entry, refusal.reason),
                is_fixable=False,
                severity=ir.IssueSeverity.ERROR,
                translation_key=refusal.reason,
                translation_placeholders={"title": entry.title, **refusal.placeholders},
            )
        raise not_set_up(refusal) from refusal
    for reason in REPAIRABLE:
        ir.async_delete_issue(hass, DOMAIN, issue_of(entry, reason))
    entry.runtime_data = Runtime(connected, technical)
    if technical is not None:
        entry.async_create_background_task(hass, technical.stream.follow(), f"{DOMAIN} stream")
        entry.async_create_background_task(hass, technical.diagnosis.async_refresh(), f"{DOMAIN} diagnosis")
        entry.async_create_background_task(hass, technical.versions.async_refresh(), f"{DOMAIN} versions")
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def set_up_technical(
    hass: HomeAssistant,
    entry: LemonfiberConfigEntry,
    connected: Connected,
) -> Technical:
    """Open the stream and wait for its first dashboard, so the entities are built from what the stack has."""
    version = await connected.version()
    stream = connected.client.events()
    stream_coordinator = StreamCoordinator(hass, entry, connected, stream, await first_snapshot(stream))
    versions = VersionsCoordinator(hass, entry, connected.client)
    return Technical(version, stream_coordinator, stream_coordinator.diagnosis, versions)


async def async_unload_entry(hass: HomeAssistant, entry: LemonfiberConfigEntry) -> bool:
    """Let the entities go; the stream and the diagnosis stop with the entry's background tasks."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
