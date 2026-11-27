# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/diagnose`, and the shapes only `/api/actions/diagnose` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class DiagnoseAction(ActionRequest):
    """The action `diagnose`, with the arguments it is posted with."""

    ACTION = "diagnose"

    only: str | None = None
    """The group of checks, or the one check, a diagnosis is narrowed to."""
    disruptive: bool
    """Whether the checks that disturb the running system are included."""


__all__ = [
    "DiagnoseAction",
]
