# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/household-approve`, and the shapes only `/api/actions/household-approve` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class HouseholdApproveAction(ActionRequest):
    """The action `household-approve`, with the arguments it is posted with."""

    ACTION = "household-approve"

    request: str | None = None
    """The request being ruled on, by the reference the household list names it with:
    the request service's own number (`42`), or `tv-<n>`, `movies-<n>`, `music-<n>` or
    `books-<n>` for an ask the core keeps.
    """
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "HouseholdApproveAction",
]
