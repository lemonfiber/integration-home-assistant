# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/hosting-remove`, and the shapes only `/api/actions/hosting-remove` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class HostingRemoveAction(ActionRequest):
    """The action `hosting-remove`, with the arguments it is posted with."""

    ACTION = "hosting-remove"

    kept: str | None = None
    """Which command this machine is being asked to keep running, or stop keeping.

    A word rather than a switch, for the reason `policy` is one: there is more than
    one of them, and a word this build does not know is refused by name rather than
    silently taken for whichever the shape happened to default to.
    """
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "HostingRemoveAction",
]
