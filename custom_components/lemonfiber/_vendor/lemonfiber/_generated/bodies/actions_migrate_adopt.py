# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/migrate-adopt`, and the shapes only `/api/actions/migrate-adopt` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class MigrateAdoptAction(ActionRequest):
    """The action `migrate-adopt`, with the arguments it is posted with. `confirm` carries the operator's yes."""

    ACTION = "migrate-adopt"

    confirm: bool = False
    """Whether a cost the action would incur was agreed to in advance."""
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "MigrateAdoptAction",
]
