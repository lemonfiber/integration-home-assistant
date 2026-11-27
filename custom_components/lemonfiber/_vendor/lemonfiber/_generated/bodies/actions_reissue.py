# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/reissue`, and the shapes only `/api/actions/reissue` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class ReissueAction(ActionRequest):
    """The action `reissue`, with the arguments it is posted with."""

    ACTION = "reissue"

    name: str | None = None
    """Who an action addressed to somebody in the household is for, as they sign in."""
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "ReissueAction",
]
