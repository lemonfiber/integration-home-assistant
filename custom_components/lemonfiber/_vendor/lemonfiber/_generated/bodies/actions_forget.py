# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/forget`, and the shapes only `/api/actions/forget` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class ForgetAction(ActionRequest):
    """The action `forget`, with the arguments it is posted with. `confirm` carries the operator's yes."""

    ACTION = "forget"

    confirm: bool = False
    """Whether a cost the action would incur was agreed to in advance."""
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "ForgetAction",
]
