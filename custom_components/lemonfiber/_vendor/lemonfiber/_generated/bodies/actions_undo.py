# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/undo`, and the shapes only `/api/actions/undo` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest
from ..shared.instant import Instant


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class UndoAction(ActionRequest):
    """The action `undo`, with the arguments it is posted with."""

    ACTION = "undo"

    at: Instant | None = None
    """When the run to put back was made, as the history writes it."""
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "UndoAction",
]
