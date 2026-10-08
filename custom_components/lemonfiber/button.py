# Copyright (c) 2026 NightWorksIO
"""The controls a press is enough for: running the doctor, and restarting one service or the whole stack."""

from typing import TYPE_CHECKING, Final, override

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.components.button.const import ButtonDeviceClass
from homeassistant.const import EntityCategory

from . import readings
from .coordinator import DiagnosisCoordinator, StreamCoordinator
from .entity import StackEntity, technical_side
from .jobs import carry_out

if TYPE_CHECKING:
    from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
    from lemonfiber.contract import Service

    from .runtime import LemonfiberConfigEntry, Technical

PARALLEL_UPDATES: Final = 1
"""One press at a time: each asks the stack for an action and follows it to the end."""

DIAGNOSE: Final = "diagnose"
"""The action that runs the doctor."""

RESTART: Final = "restart"
"""The action that restarts the services it is given."""

RUN_THE_DOCTOR: Final = ButtonEntityDescription(key="run_the_doctor", translation_key="run_the_doctor")

RESTART_STACK: Final = ButtonEntityDescription(
    key="stack_restart",
    translation_key="restart_stack",
    device_class=ButtonDeviceClass.RESTART,
    entity_category=EntityCategory.CONFIG,
)

RESTART_SERVICE: Final = "restart_service"
"""The translation every service's restart button is named by, with the service's name in it."""


@technical_side
async def async_setup_entry(
    entry: LemonfiberConfigEntry,
    technical: Technical,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add the doctor's button, and a restart button for the stack and for every service the dashboard names, each where the key may call its action."""
    connected = entry.runtime_data.connected
    buttons: list[ButtonEntity] = []
    if connected.may_call(DIAGNOSE):
        buttons.append(RunTheDoctor(technical, entry))
    if connected.may_call(RESTART):
        buttons.append(RestartStack(technical.stream, entry, technical, RESTART_STACK))
        buttons.extend(
            RestartService(technical, entry, service) for service in readings.services(technical.stream.data)
        )
    async_add_entities(buttons)


class RunTheDoctor(StackEntity[StreamCoordinator], ButtonEntity):
    """Run every check the doctor has, follow the run to its end, and read the findings it came to.

    Available while the stream is, whatever became of the last reading of the findings.
    """

    def __init__(self, technical: Technical, entry: LemonfiberConfigEntry) -> None:
        """Attach the button to the stack's stream, and to the findings it has read again."""
        super().__init__(technical.stream, entry, technical, RUN_THE_DOCTOR)
        self._diagnosis: DiagnosisCoordinator = technical.diagnosis

    @override
    async def async_press(self) -> None:
        await carry_out(self.hass, self.coordinator.config_entry, DIAGNOSE)
        await self._diagnosis.async_request_refresh()


class RestartStack(StackEntity[StreamCoordinator], ButtonEntity):
    """Restart every service the stack runs, and follow the restart to its end."""

    @override
    async def async_press(self) -> None:
        await carry_out(self.hass, self.coordinator.config_entry, RESTART)


class RestartService(StackEntity[StreamCoordinator], ButtonEntity):
    """Restart one service, leaving the rest of its form alone, and follow the restart to its end.

    Left off until enabled: restarting the stack is the control most people
    want, and one button per service is there for whoever wants that reach.
    """

    def __init__(self, technical: Technical, entry: LemonfiberConfigEntry, service: Service) -> None:
        """Name the button for the service it restarts."""
        description = ButtonEntityDescription(
            key=f"restart_{service['id']}",
            translation_key=RESTART_SERVICE,
            device_class=ButtonDeviceClass.RESTART,
            entity_category=EntityCategory.CONFIG,
            entity_registry_enabled_default=False,
        )
        super().__init__(technical.stream, entry, technical, description)
        self._service = service["id"]
        self._attr_translation_placeholders = {"service": service["name"]}

    @override
    async def async_press(self) -> None:
        await carry_out(self.hass, self.coordinator.config_entry, RESTART, {"services": [self._service]})
