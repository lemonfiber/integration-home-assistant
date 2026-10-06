# Copyright (c) 2026 NightWorksIO
"""The controls a press is enough for: running the doctor."""

from typing import TYPE_CHECKING, Final, override

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription

from .coordinator import DiagnosisCoordinator, StreamCoordinator
from .entity import StackEntity, technical_side
from .jobs import carry_out

if TYPE_CHECKING:
    from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

    from .runtime import LemonfiberConfigEntry, Technical

PARALLEL_UPDATES: Final = 1
"""One press at a time: each asks the stack for an action and follows it to the end."""

DIAGNOSE: Final = "diagnose"
"""The action that runs the doctor."""

RUN_THE_DOCTOR: Final = ButtonEntityDescription(key="run_the_doctor", translation_key="run_the_doctor")


@technical_side
async def async_setup_entry(
    entry: LemonfiberConfigEntry,
    technical: Technical,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add the doctor's button, where the key may run the doctor."""
    if entry.runtime_data.connected.may_call(DIAGNOSE):
        async_add_entities([RunTheDoctor(technical, entry)])


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
