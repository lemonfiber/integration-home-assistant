# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/migrate-import`, and the shapes only `/api/actions/migrate-import` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class MigrateImportAction(ActionRequest):
    """The action `migrate-import`, with the arguments it is posted with. `confirm` carries the operator's yes."""

    ACTION = "migrate-import"

    confirm: bool = False
    """Whether a cost the action would incur was agreed to in advance."""
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "MigrateImportAction",
]
