# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/quality-reapply`, and the shapes only `/api/actions/quality-reapply` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class QualityReapplyAction(ActionRequest):
    """The action `quality-reapply`, with the arguments it is posted with."""

    ACTION = "quality-reapply"

    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "QualityReapplyAction",
]
