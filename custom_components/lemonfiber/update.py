# Copyright (c) 2026 NightWorksIO
"""One update entity for every service the stack runs: the tag it stands on, and the tag this build pins."""

from typing import TYPE_CHECKING, Final, override

from homeassistant.components.update import UpdateEntity, UpdateEntityDescription
from homeassistant.core import callback

from . import readings
from .coordinator import VersionsCoordinator
from .entity import StackEntity, technical_side

if TYPE_CHECKING:
    from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
    from lemonfiber.contract import Service

    from .runtime import LemonfiberConfigEntry, Technical

PARALLEL_UPDATES: Final = 0
"""Every entity here is updated by its coordinator, so none of them asks the stack anything itself."""

SERVICE_UPDATE: Final = "service_update"
"""The translation every service's update entity is named by, with the service's name in it."""


@technical_side
async def async_setup_entry(
    entry: LemonfiberConfigEntry,
    technical: Technical,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add an update entity for every service the dashboard names."""
    async_add_entities(
        ServiceUpdate(technical.versions, entry, technical, service)
        for service in readings.services(technical.stream.data)
    )


class ServiceUpdate(StackEntity[VersionsCoordinator], UpdateEntity):
    """Where one service stands against the tag this build pins it at; unknown until the versions are first read."""

    def __init__(
        self,
        coordinator: VersionsCoordinator,
        entry: LemonfiberConfigEntry,
        technical: Technical,
        service: Service,
    ) -> None:
        """Name the entity for the service and read its versions."""
        description = UpdateEntityDescription(key=f"update_{service['id']}", translation_key=SERVICE_UPDATE)
        super().__init__(coordinator, entry, technical, description)
        self._service = service["id"]
        self._attr_title = service["name"]
        self._attr_translation_placeholders = {"service": service["name"]}
        self._read()

    def _read(self) -> None:
        versions = self.coordinator.data
        self._attr_installed_version = None if versions is None else versions.installed(self._service)
        self._attr_latest_version = None if versions is None else versions.pinned.get(self._service)

    @callback
    @override
    def _handle_coordinator_update(self) -> None:
        self._read()
        super()._handle_coordinator_update()
