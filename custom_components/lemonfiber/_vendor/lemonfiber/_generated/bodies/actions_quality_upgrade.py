# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/quality-upgrade`, and the shapes only `/api/actions/quality-upgrade` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class QualityUpgradeAction(ActionRequest):
    """The action `quality-upgrade`, with the arguments it is posted with. `confirm` carries the operator's yes."""

    ACTION = "quality-upgrade"

    confirm: bool = False
    """Whether a cost the action would incur was agreed to in advance."""
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "QualityUpgradeAction",
]
