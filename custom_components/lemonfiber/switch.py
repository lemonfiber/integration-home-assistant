# Copyright (c) 2026 NightWorksIO
"""Pausing and resuming every download client, shown as the last thing asked of them."""

from typing import TYPE_CHECKING, Any, Final, override

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription

from .coordinator import StreamCoordinator
from .entity import StackEntity, technical_side
from .jobs import carry_out

if TYPE_CHECKING:
    from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

    from .runtime import LemonfiberConfigEntry, Technical

PARALLEL_UPDATES: Final = 1
"""One toggle at a time: each asks the stack for an action and follows it to the end."""

PAUSE: Final = "downloads-pause"
RESUME: Final = "downloads-resume"

DOWNLOADS_PAUSED: Final = SwitchEntityDescription(key="downloads_paused", translation_key="downloads_paused")


@technical_side
async def async_setup_entry(
    entry: LemonfiberConfigEntry,
    technical: Technical,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add the downloads switch, where the key may both pause and resume them."""
    connected = entry.runtime_data.connected
    if connected.may_call(PAUSE) and connected.may_call(RESUME):
        async_add_entities([DownloadsPaused(technical.stream, entry, technical, DOWNLOADS_PAUSED)])


class DownloadsPaused(StackEntity[StreamCoordinator], SwitchEntity):
    """On once every download client has been asked to pause, off once asked to resume.

    The stack reports no paused state, so the switch shows what it last asked
    for, and is unknown until it has asked anything.
    """

    _attr_assumed_state = True

    async def _ask(self, action: str, *, paused: bool) -> None:
        await carry_out(self.hass, self.coordinator.config_entry, action)
        self._attr_is_on = paused
        self.async_write_ha_state()

    @override
    async def async_turn_on(self, **kwargs: Any) -> None:
        await self._ask(PAUSE, paused=True)

    @override
    async def async_turn_off(self, **kwargs: Any) -> None:
        await self._ask(RESUME, paused=False)
