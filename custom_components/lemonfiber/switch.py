# Copyright (c) 2026 NightWorksIO
"""Pausing and resuming every download client, shown as the clients read it back."""

from typing import TYPE_CHECKING, Any, Final, override

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.core import callback

from . import readings
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
    """On while the download clients say they are paused, off while any says it is fetching.

    Turning it on or off asks every client to pause or resume, and the switch
    then shows what the clients read back on the stream, not what it asked for.
    Unknown where no client could be asked.
    """

    def __init__(
        self,
        coordinator: StreamCoordinator,
        entry: LemonfiberConfigEntry,
        technical: Technical,
        description: SwitchEntityDescription,
    ) -> None:
        """Describe the switch and read the clients from the dashboard the stream last carried."""
        super().__init__(coordinator, entry, technical, description)
        self._attr_is_on = readings.paused(coordinator.data)

    @callback
    @override
    def _handle_coordinator_update(self) -> None:
        self._attr_is_on = readings.paused(self.coordinator.data)
        super()._handle_coordinator_update()

    @override
    async def async_turn_on(self, **kwargs: Any) -> None:
        await carry_out(self.hass, self.coordinator.config_entry, PAUSE)

    @override
    async def async_turn_off(self, **kwargs: Any) -> None:
        await carry_out(self.hass, self.coordinator.config_entry, RESUME)
