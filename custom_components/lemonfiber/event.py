# Copyright (c) 2026 NightWorksIO
"""The stack's alerts as an event entity: each onset and resolution, in the stack's own words."""

import typing
from typing import TYPE_CHECKING, Final, override

from homeassistant.components.event import EventEntity, EventEntityDescription
from homeassistant.core import callback
from lemonfiber.contract import Moment

from .alerts import told
from .coordinator import StreamCoordinator
from .entity import StackEntity, technical_side

if TYPE_CHECKING:
    from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
    from lemonfiber.contract import Alert

    from .runtime import LemonfiberConfigEntry, Technical

PARALLEL_UPDATES: Final = 0
"""The entity is written by the stream, so it asks the stack nothing itself."""

MOMENTS: Final[list[str]] = list(typing.get_args(Moment.__value__))
"""Every way an alert can go, each an event type: its onset, and its resolution."""

ALERTS: Final = EventEntityDescription(key="alerts", translation_key="alerts", event_types=MOMENTS)


@technical_side
async def async_setup_entry(
    entry: LemonfiberConfigEntry,
    technical: Technical,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add the stack's alerts."""
    async_add_entities([StackAlerts(technical.stream, entry, technical, ALERTS)])


class StackAlerts(StackEntity[StreamCoordinator], EventEntity):
    """The last alert the stream carried, its moment as the event type and what it said as the attributes."""

    @override
    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        self.async_on_remove(self.coordinator.async_add_alert_listener(self._alerted))

    @callback
    def _alerted(self, alert: Alert) -> None:
        said = told(alert)
        moment = said.pop("moment")
        self._trigger_event(str(moment), said)
        self.async_write_ha_state()
