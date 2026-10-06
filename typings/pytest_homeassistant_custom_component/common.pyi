# Copyright (c) 2026 NightWorksIO
# The part of the test harness the suite uses, with the types it has.

from collections.abc import Mapping
from datetime import datetime
from typing import Any

from homeassistant.config_entries import ConfigEntry, ConfigFlowResult
from homeassistant.core import Event, HomeAssistant

class MockConfigEntry(ConfigEntry):
    def __init__(
        self,
        *,
        domain: str = ...,
        title: str = ...,
        unique_id: str | None = ...,
        data: Mapping[str, Any] | None = ...,
    ) -> None: ...
    def add_to_hass(self, hass: HomeAssistant) -> None: ...
    async def start_reauth_flow(self, hass: HomeAssistant) -> ConfigFlowResult: ...
    async def start_reconfigure_flow(self, hass: HomeAssistant) -> ConfigFlowResult: ...

def async_fire_time_changed(
    hass: HomeAssistant,
    datetime_: datetime | None = ...,
    fire_all: bool = ...,
) -> None: ...
def async_capture_events(hass: HomeAssistant, event_name: str) -> list[Event[Any]]: ...
