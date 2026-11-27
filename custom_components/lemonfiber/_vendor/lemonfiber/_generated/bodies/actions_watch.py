# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/watch`, and the shapes only `/api/actions/watch` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class WatchAction(ActionRequest):
    """The action `watch`, with the arguments it is posted with."""

    ACTION = "watch"

    forms: list[str] = dataclasses.field(default_factory=lambda: [])
    """The forms to act on."""
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "WatchAction",
]
