# Copyright (c) 2026 NightWorksIO
"""What every entity of a stack shares: its device, and how it is named and identified, on the technical side and on a member's own."""

from typing import TYPE_CHECKING, Any, override

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER, MODEL

if TYPE_CHECKING:
    from collections.abc import Callable, Coroutine

    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity import EntityDescription
    from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
    from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

    from .coordinator import StreamCoordinator
    from .member import MemberCoordinator
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


type MemberSetup = Callable[
    [LemonfiberConfigEntry, MemberCoordinator, AddConfigEntryEntitiesCallback],
    Coroutine[Any, Any, None],
]
"""What a platform adds of a member's own side."""


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


def member_side(adds: MemberSetup) -> PlatformSetup:
    """Return a platform's setup that adds its entities only for a member's key, from that member's own stream.

    A `read` or `act` key yields no member's entity, so a platform built this
    way adds nothing for one.
    """

    async def async_setup_entry(
        _hass: HomeAssistant,
        entry: LemonfiberConfigEntry,
        async_add_entities: AddConfigEntryEntitiesCallback,
    ) -> None:
        theirs = entry.runtime_data.theirs
        if theirs is not None:
            await adds(entry, theirs, async_add_entities)

    return async_setup_entry


def both(*setups: PlatformSetup) -> PlatformSetup:
    """Return a platform's setup that runs each of these in turn, for a platform with entities on both sides."""

    async def async_setup_entry(
        hass: HomeAssistant,
        entry: LemonfiberConfigEntry,
        async_add_entities: AddConfigEntryEntitiesCallback,
    ) -> None:
        for setup in setups:
            await setup(hass, entry, async_add_entities)

    return async_setup_entry


def theirs_device(entry: LemonfiberConfigEntry) -> DeviceInfo:
    """Return the one device a member's entry is, naming nothing technical: no version and no address."""
    return DeviceInfo(
        identifiers={(DOMAIN, entry.entry_id)},
        name=entry.title,
        manufacturer=MANUFACTURER,
        model=MODEL,
    )


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
    """An entity of the stack, named by its translation and identified within its entry.

    It is unavailable whenever the stream has a gap, whatever its own coordinator
    holds: a value gathered before the gap is not shown as current.
    """

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: CoordinatorT,
        entry: LemonfiberConfigEntry,
        technical: Technical,
        description: EntityDescription,
    ) -> None:
        """Describe the entity, attach it to the stack's device, and follow the stream's gaps."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}-{description.key}"
        self._attr_device_info = device_of(entry, technical.version)
        self._stream: StreamCoordinator = technical.stream

    @property
    @override
    def available(self) -> bool:
        return super().available and self._stream.last_update_success

    @override
    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        if self.coordinator is not self._stream:
            self.async_on_remove(self._stream.async_add_listener(self.async_write_ha_state))


class MemberEntity(CoordinatorEntity["MemberCoordinator"]):
    """An entity of a member's own side, named by its translation and identified within its entry."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MemberCoordinator,
        entry: LemonfiberConfigEntry,
        description: EntityDescription,
    ) -> None:
        """Describe the entity and attach it to the entry's device."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}-{description.key}"
        self._attr_device_info = theirs_device(entry)
