# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/household-decline`, and the shapes only `/api/actions/household-decline` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class HouseholdDeclineAction(ActionRequest):
    """The action `household-decline`, with the arguments it is posted with."""

    ACTION = "household-decline"

    request: str | None = None
    """The request being ruled on, by the reference the household list names it with:
    the request service's own number (`42`), or `tv-<n>`, `movies-<n>`, `music-<n>` or
    `books-<n>` for an ask the core keeps.
    """
    reason: str | None = None
    """Why a request is being turned down, or why a service was chosen to fill a
    capability.
    """
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "HouseholdDeclineAction",
]
