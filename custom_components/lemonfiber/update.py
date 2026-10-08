# Copyright (c) 2026 NightWorksIO
"""An update entity for the whole stack and for every service it runs: the tags they stand on, the tags this build pins, and taking the step between them."""

from typing import TYPE_CHECKING, Any, Final, override

from homeassistant.components.update import UpdateEntity, UpdateEntityDescription, UpdateEntityFeature
from homeassistant.core import callback

from . import readings
from .coordinator import VersionsCoordinator
from .entity import StackEntity, technical_side
from .jobs import carry_out

if TYPE_CHECKING:
    from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
    from lemonfiber.contract import Service, UpdateChange

    from .runtime import LemonfiberConfigEntry, Technical

PARALLEL_UPDATES: Final = 1
"""One install at a time: each asks the stack to update itself or a service, and follows it to the end."""

SERVICE_UPDATE: Final = "service_update"
"""The translation every service's update entity is named by, with the service's name in it."""

UPDATE: Final = "update"
"""The action that updates the stack, or one service of it, to the tags this build pins."""

STACK_UPDATE: Final = UpdateEntityDescription(key="stack_update", translation_key="stack_update")


@technical_side
async def async_setup_entry(
    entry: LemonfiberConfigEntry,
    technical: Technical,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add an update entity for the stack and for every service the dashboard names, able to install where the key may update."""
    installs = entry.runtime_data.connected.may_call(UPDATE)
    async_add_entities(
        [
            StackUpdate(technical.versions, entry, technical, installs=installs),
            *(
                ServiceUpdate(technical.versions, entry, technical, service, installs=installs)
                for service in readings.services(technical.stream.data)
            ),
        ],
    )


class ServiceUpdate(StackEntity[VersionsCoordinator], UpdateEntity):
    """Where one service stands against the tag this build pins it at; unknown until the versions are first read.

    Installing asks the stack to update the one service, agreeing to what the
    step costs, since pressing install is that agreement. A step the stack
    refuses to take is offered as no install at all. Left off until enabled: the
    stack's own update entity is the one most people want.
    """

    def __init__(
        self,
        coordinator: VersionsCoordinator,
        entry: LemonfiberConfigEntry,
        technical: Technical,
        service: Service,
        *,
        installs: bool,
    ) -> None:
        """Name the entity for the service and read its versions."""
        description = UpdateEntityDescription(
            key=f"update_{service['id']}",
            translation_key=SERVICE_UPDATE,
            entity_registry_enabled_default=False,
        )
        super().__init__(coordinator, entry, technical, description)
        self._service = service["id"]
        self._installs = installs
        self._attr_title = service["name"]
        self._attr_translation_placeholders = {"service": service["name"]}
        self._read()

    def _read(self) -> None:
        versions = self.coordinator.data
        change = None if versions is None else versions.changes.get(self._service)
        self._attr_installed_version = None if versions is None else versions.installed(self._service)
        self._attr_latest_version = None if versions is None else versions.pinned.get(self._service)
        self._attr_release_summary = None if change is None else change["because"] or None
        takeable = self._installs and change is not None and not change["refused"]
        self._attr_supported_features = UpdateEntityFeature.INSTALL if takeable else UpdateEntityFeature(0)

    @callback
    @override
    def _handle_coordinator_update(self) -> None:
        self._read()
        super()._handle_coordinator_update()

    @override
    async def async_install(self, version: str | None, backup: bool, **kwargs: Any) -> None:
        try:
            await carry_out(
                self.hass,
                self.coordinator.config_entry,
                UPDATE,
                {"service": self._service, "confirm": True},
            )
        finally:
            await self.coordinator.async_request_refresh()


class StackUpdate(StackEntity[VersionsCoordinator], UpdateEntity):
    """Every service that is off its pin, and taking all of their steps in one update of the stack.

    Where nothing would move, the stack stands on what this build of lemonfiber
    pins, and both versions are that build's. Otherwise each side names every
    service that would move, by its id, at the tag it stands on and the tag it
    would move to.
    """

    def __init__(
        self,
        coordinator: VersionsCoordinator,
        entry: LemonfiberConfigEntry,
        technical: Technical,
        *,
        installs: bool,
    ) -> None:
        """Describe the stack's update and read what it would move."""
        super().__init__(coordinator, entry, technical, STACK_UPDATE)
        self._build = technical.version
        self._installs = installs
        self._changes: list[UpdateChange] = []
        self._read()

    def _read(self) -> None:
        versions = self.coordinator.data
        self._changes = (
            [] if versions is None else sorted(versions.changes.values(), key=lambda one: one["service"])
        )
        if versions is None:
            self._attr_installed_version = self._attr_latest_version = None
        elif not self._changes:
            self._attr_installed_version = self._attr_latest_version = self._build
        else:
            self._attr_installed_version = ", ".join(
                f"{one['service']} {one['current']}" for one in self._changes
            )
            self._attr_latest_version = ", ".join(
                f"{one['service']} {one['target']}" for one in self._changes
            )
        takeable = self._installs and any(not one["refused"] for one in self._changes)
        features = UpdateEntityFeature.RELEASE_NOTES
        self._attr_supported_features = features | UpdateEntityFeature.INSTALL if takeable else features

    @callback
    @override
    def _handle_coordinator_update(self) -> None:
        self._read()
        super()._handle_coordinator_update()

    @override
    def version_is_newer(self, latest_version: str, installed_version: str) -> bool:
        """Tell that the stack has an update wherever the two sides differ: they name services, not one version."""
        return latest_version != installed_version

    @override
    async def async_release_notes(self) -> str | None:
        """Return each step the update would take and what it means, in the stack's words."""
        if not self._changes:
            return None
        return "\n".join(
            f"- **{one['service']}** {one['current']} → {one['target']}: {one['because']}"
            for one in self._changes
        )

    @override
    async def async_install(self, version: str | None, backup: bool, **kwargs: Any) -> None:
        try:
            await carry_out(self.hass, self.coordinator.config_entry, UPDATE, {"confirm": True})
        finally:
            await self.coordinator.async_request_refresh()
