# Copyright (c) 2026 NightWorksIO
"""The stack's yes-or-no answers: whether anything is wrong, whether downloads leave through the VPN, and whether each download client is paused."""

from dataclasses import dataclass, field
from functools import partial
from typing import TYPE_CHECKING, Final, override

from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorEntityDescription
from homeassistant.components.binary_sensor.const import BinarySensorDeviceClass
from homeassistant.const import EntityCategory
from homeassistant.core import callback

from . import readings
from .coordinator import StreamCoordinator
from .entity import StackEntity, technical_side

if TYPE_CHECKING:
    from collections.abc import Callable

    from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
    from lemonfiber.contract import Snapshot

    from .runtime import LemonfiberConfigEntry, Technical

PARALLEL_UPDATES: Final = 0
"""Every entity here is updated by its coordinator, so none of them asks the stack anything itself."""


def always(_: Snapshot) -> bool:
    """Return that every stack has this entity."""
    return True


@dataclass(frozen=True, kw_only=True)
class DashboardBinarySensorDescription(BinarySensorEntityDescription):
    """A yes or no the dashboard carries, None where the stack cannot say, and whether a stack has it at all."""

    value: Callable[[Snapshot], bool | None]
    exists: Callable[[Snapshot], bool] = field(default=always)


DASHBOARD_BINARY_SENSORS: Final = (
    DashboardBinarySensorDescription(
        key="health_problem",
        translation_key="health_problem",
        device_class=BinarySensorDeviceClass.PROBLEM,
        value=readings.wanting_attention,
    ),
    DashboardBinarySensorDescription(
        key="vpn",
        translation_key="vpn",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        value=readings.vpn_up,
        exists=readings.has_vpn,
    ),
)


CLIENT_PAUSED: Final = "client_paused"
"""The translation each download client's paused state is named by, with the client's name in it."""


@technical_side
async def async_setup_entry(
    entry: LemonfiberConfigEntry,
    technical: Technical,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add the stack's yes-or-no answers that apply to it."""
    snapshot = technical.stream.data
    async_add_entities(
        [
            *(
                DashboardBinarySensor(technical.stream, entry, technical, one)
                for one in DASHBOARD_BINARY_SENSORS
                if one.exists(snapshot)
            ),
            *(
                DashboardBinarySensor(technical.stream, entry, technical, client_paused(one["client"]))
                for one in readings.downloaders(snapshot)
            ),
        ],
    )


def client_paused(client: str) -> DashboardBinarySensorDescription:
    """Describe whether one download client says it is paused: a diagnostic, left off until enabled."""
    return DashboardBinarySensorDescription(
        key=f"paused_{client}",
        translation_key=CLIENT_PAUSED,
        translation_placeholders={"client": client},
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        value=partial(readings.client_paused, client=client),
    )


class DashboardBinarySensor(StackEntity[StreamCoordinator], BinarySensorEntity):
    """A yes or no from the dashboard: unavailable from a gap in the stream, unknown where the stack cannot say."""

    def __init__(
        self,
        coordinator: StreamCoordinator,
        entry: LemonfiberConfigEntry,
        technical: Technical,
        description: DashboardBinarySensorDescription,
    ) -> None:
        """Describe the answer and read it from the dashboard the stream last carried."""
        super().__init__(coordinator, entry, technical, description)
        self._reading = description
        self._attr_is_on = description.value(coordinator.data)

    @callback
    @override
    def _handle_coordinator_update(self) -> None:
        self._attr_is_on = self._reading.value(self.coordinator.data)
        super()._handle_coordinator_update()
