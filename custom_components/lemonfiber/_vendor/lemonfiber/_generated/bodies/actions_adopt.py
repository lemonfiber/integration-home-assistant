# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/adopt`, and the shapes only `/api/actions/adopt` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class AdoptAction(ActionRequest):
    """The action `adopt`, with the arguments it is posted with."""

    ACTION = "adopt"

    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "AdoptAction",
]
