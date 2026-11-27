# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/backup`, and the shapes only `/api/actions/backup` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class BackupAction(ActionRequest):
    """The action `backup`, with the arguments it is posted with."""

    ACTION = "backup"

    service: str | None = None
    """The one service to act on instead of the whole stack."""
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "BackupAction",
]
