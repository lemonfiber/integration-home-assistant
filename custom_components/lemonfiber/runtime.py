# Copyright (c) 2026 NightWorksIO
"""What a loaded entry holds while it runs."""

from dataclasses import dataclass
from typing import TYPE_CHECKING

from homeassistant.config_entries import ConfigEntry

if TYPE_CHECKING:
    from .connection import Connected
    from .coordinator import DiagnosisCoordinator, StreamCoordinator, VersionsCoordinator
    from .member import MemberCoordinator


@dataclass(frozen=True, slots=True)
class Technical:
    """What a `read` or `act` key follows: the version the stack runs, its stream, the doctor's findings and the services' versions."""

    version: str
    stream: StreamCoordinator
    diagnosis: DiagnosisCoordinator
    versions: VersionsCoordinator


@dataclass(frozen=True, slots=True)
class Runtime:
    """The client that reached the stack, and the side of it the key's scope reaches: the technical one, or a member's own."""

    connected: Connected
    technical: Technical | None
    """Absent for a member's key, which yields no technical entity."""
    theirs: MemberCoordinator | None = None
    """A member's own stream, present for a member's key alone."""


type LemonfiberConfigEntry = ConfigEntry[Runtime]
