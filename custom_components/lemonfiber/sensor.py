# Copyright (c) 2026 NightWorksIO
"""The stack's figures: its health, its downloads, its disk, and the doctor's findings by severity; and a member's requests by state."""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Final, override

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import UnitOfDataRate, UnitOfInformation
from homeassistant.core import callback

from . import readings
from .coordinator import DiagnosisCoordinator, StreamCoordinator
from .entity import MemberEntity, StackEntity, both, member_side, technical_side
from .member import GONE, REQUEST_STATES, MemberCoordinator

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
    from homeassistant.helpers.typing import StateType
    from lemonfiber.contract import ProblemSeverity, RequestState, Snapshot

    from .runtime import LemonfiberConfigEntry, Technical

PARALLEL_UPDATES: Final = 0
"""Every entity here is updated by its coordinator, so none of them asks the stack anything itself."""


def no_attributes(_: Snapshot) -> Mapping[str, object]:
    """Return nothing beside the value."""
    return {}


@dataclass(frozen=True, kw_only=True)
class DashboardSensorDescription(SensorEntityDescription):
    """A figure the dashboard carries, None where the stack cannot say what it is now."""

    value: Callable[[Snapshot], StateType]
    attributes: Callable[[Snapshot], Mapping[str, object]] = field(default=no_attributes)


DASHBOARD_SENSORS: Final = (
    DashboardSensorDescription(
        key="health",
        translation_key="health",
        device_class=SensorDeviceClass.ENUM,
        options=list(readings.STANDINGS),
        value=readings.health,
        attributes=readings.worst,
    ),
    DashboardSensorDescription(
        key="download_queue",
        translation_key="download_queue",
        state_class=SensorStateClass.MEASUREMENT,
        value=readings.queued,
    ),
    DashboardSensorDescription(
        key="download_speed",
        translation_key="download_speed",
        device_class=SensorDeviceClass.DATA_RATE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfDataRate.BYTES_PER_SECOND,
        suggested_unit_of_measurement=UnitOfDataRate.MEGABYTES_PER_SECOND,
        value=readings.speed,
    ),
    DashboardSensorDescription(
        key="disk_free_data",
        translation_key="disk_free_data",
        device_class=SensorDeviceClass.DATA_SIZE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfInformation.BYTES,
        suggested_unit_of_measurement=UnitOfInformation.GIGABYTES,
        value=readings.disk_free,
    ),
)


@dataclass(frozen=True, kw_only=True)
class FindingsSensorDescription(SensorEntityDescription):
    """How many of the doctor's findings carry one severity."""

    severity: ProblemSeverity


FINDINGS_SENSORS: Final = tuple(
    FindingsSensorDescription(
        key=f"findings_{severity}",
        translation_key=f"findings_{severity}",
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=severity != readings.LEAST_SEVERE,
        severity=severity,
    )
    for severity in readings.SEVERITIES
)


@dataclass(frozen=True, kw_only=True)
class RequestsSensorDescription(SensorEntityDescription):
    """How many of a member's requests stand at one state."""

    state: RequestState


REQUESTS_SENSORS: Final = tuple(
    RequestsSensorDescription(
        key=f"requests_{state.replace('-', '_')}",
        translation_key=f"requests_{state.replace('-', '_')}",
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=state != GONE,
        state=state,
    )
    for state in REQUEST_STATES
)


@technical_side
async def add_technical(
    entry: LemonfiberConfigEntry,
    technical: Technical,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add the stack's figures."""
    async_add_entities(
        [
            *(DashboardSensor(technical.stream, entry, technical, one) for one in DASHBOARD_SENSORS),
            *(FindingsSensor(technical.diagnosis, entry, technical, one) for one in FINDINGS_SENSORS),
        ],
    )


@member_side
async def add_theirs(
    entry: LemonfiberConfigEntry,
    theirs: MemberCoordinator,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add a member's requests, by the state each stands at."""
    async_add_entities(RequestsSensor(theirs, entry, one) for one in REQUESTS_SENSORS)


async_setup_entry: Final = both(add_technical, add_theirs)


class DashboardSensor(StackEntity[StreamCoordinator], SensorEntity):
    """A figure from the dashboard: unavailable from a gap in the stream, unknown where the stack cannot say."""

    def __init__(
        self,
        coordinator: StreamCoordinator,
        entry: LemonfiberConfigEntry,
        technical: Technical,
        description: DashboardSensorDescription,
    ) -> None:
        """Describe the figure and read it from the dashboard the stream last carried."""
        super().__init__(coordinator, entry, technical, description)
        self._reading = description
        self._read()

    def _read(self) -> None:
        snapshot = self.coordinator.data
        self._attr_native_value = self._reading.value(snapshot)
        self._attr_extra_state_attributes = dict(self._reading.attributes(snapshot))

    @callback
    @override
    def _handle_coordinator_update(self) -> None:
        self._read()
        super()._handle_coordinator_update()


class FindingsSensor(StackEntity[DiagnosisCoordinator], SensorEntity):
    """How many findings carry a severity, and what each says happened; unknown until the doctor is first read."""

    def __init__(
        self,
        coordinator: DiagnosisCoordinator,
        entry: LemonfiberConfigEntry,
        technical: Technical,
        description: FindingsSensorDescription,
    ) -> None:
        """Describe the severity and count it in the findings last read."""
        super().__init__(coordinator, entry, technical, description)
        self._severity: ProblemSeverity = description.severity
        self._read()

    def _read(self) -> None:
        report = self.coordinator.data
        said = None if report is None else readings.findings(report, self._severity)
        self._attr_native_value = None if said is None else len(said)
        self._attr_extra_state_attributes = {} if said is None else {"findings": said}

    @callback
    @override
    def _handle_coordinator_update(self) -> None:
        self._read()
        super()._handle_coordinator_update()


class RequestsSensor(MemberEntity, SensorEntity):
    """How many of a member's requests stand at a state, and what each is called where it has a name yet.

    Unavailable until their stream has said their household row, and wherever
    the row could not be read.
    """

    def __init__(
        self,
        coordinator: MemberCoordinator,
        entry: LemonfiberConfigEntry,
        description: RequestsSensorDescription,
    ) -> None:
        """Describe the state and count their requests at it."""
        super().__init__(coordinator, entry, description)
        self._state: RequestState = description.state
        self._read()

    def _read(self) -> None:
        requests = self.coordinator.data.requests(self._state)
        self._readable = requests is not None
        self._attr_native_value = None if requests is None else len(requests)
        titles = [] if requests is None else [title for one in requests if (title := one.get("title"))]
        self._attr_extra_state_attributes = {"titles": titles}

    @property
    @override
    def available(self) -> bool:
        return super().available and self._readable

    @callback
    @override
    def _handle_coordinator_update(self) -> None:
        self._read()
        super()._handle_coordinator_update()
