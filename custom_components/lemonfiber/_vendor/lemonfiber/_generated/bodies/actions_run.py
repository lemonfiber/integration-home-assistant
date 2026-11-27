# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/run`, and the shapes only `/api/actions/run` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class RunAction(ActionRequest):
    """The action `run`, with the arguments it is posted with."""

    ACTION = "run"

    service: str | None = None
    """The one service to act on instead of the whole stack."""
    now: bool = False
    """Whether a run-and-exit service runs at once, whether or not one of its times fell
    due.
    """
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "RunAction",
]
