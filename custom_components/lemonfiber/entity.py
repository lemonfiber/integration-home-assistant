# Copyright (c) 2026 NightWorksIO
"""What every entity of a stack shares: its device, and how it is named and identified."""

from typing import TYPE_CHECKING, Any

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER, MODEL

if TYPE_CHECKING:
    from collections.abc import Callable, Coroutine

    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity import EntityDescription
    from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
    from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

    from .runtime import LemonfiberConfigEntry, Technical

type PlatformSetup = Callable[
    [HomeAssistant, LemonfiberConfigEntry, AddConfigEntryEntitiesCallback],
    Coroutine[Any, Any, None],
]
"""A platform's `async_setup_entry`, as Home Assistant calls it."""

type TechnicalSetup = Callable[
    [LemonfiberConfigEntry, Technical, AddConfigEntryEntitiesCallback],
    Coroutine[Any, Any, None],
]
"""What a platform adds of the stack's technical side."""


def technical_side(adds: TechnicalSetup) -> PlatformSetup:
    """Return a platform's setup that adds its entities only where the key reaches the stack's technical side.

    A member's key yields no technical entity, so a platform built this way adds
    nothing for one.
    """

    async def async_setup_entry(
        _hass: HomeAssistant,
        entry: LemonfiberConfigEntry,
        async_add_entities: AddConfigEntryEntitiesCallback,
    ) -> None:
        technical = entry.runtime_data.technical
        if technical is not None:
            await adds(entry, technical, async_add_entities)

    return async_setup_entry


def device_of(entry: LemonfiberConfigEntry, version: str) -> DeviceInfo:
    """Return the one device a stack is, under the entry that reaches it."""
    return DeviceInfo(
        identifiers={(DOMAIN, entry.entry_id)},
        name=entry.title,
        manufacturer=MANUFACTURER,
        model=MODEL,
        sw_version=version,
        configuration_url=entry.runtime_data.connected.client.address.base,
    )


class StackEntity[CoordinatorT: DataUpdateCoordinator[Any]](CoordinatorEntity[CoordinatorT]):
    """An entity of the stack, named by its translation and identified within its entry."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: CoordinatorT,
        entry: LemonfiberConfigEntry,
        version: str,
        description: EntityDescription,
    ) -> None:
        """Describe the entity and attach it to the stack's device."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}-{description.key}"
        self._attr_device_info = device_of(entry, version)
