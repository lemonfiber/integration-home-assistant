# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/migrate-beside`, and the shapes only `/api/actions/migrate-beside` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class MigrateBesideAction(ActionRequest):
    """The action `migrate-beside`, with the arguments it is posted with. `confirm` carries the operator's yes."""

    ACTION = "migrate-beside"

    confirm: bool = False
    """Whether a cost the action would incur was agreed to in advance."""
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "MigrateBesideAction",
]
