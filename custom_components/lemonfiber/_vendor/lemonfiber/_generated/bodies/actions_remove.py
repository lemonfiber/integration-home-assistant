# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/remove`, and the shapes only `/api/actions/remove` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class RemoveAction(ActionRequest):
    """The action `remove`, with the arguments it is posted with. `offer` carries the operator's yes."""

    ACTION = "remove"

    name: str | None = None
    """Who an action addressed to somebody in the household is for, as they sign in."""
    offer: str | None = None
    """What was read before answering — the offer a repair's yes was read in, the
    listing a restore's was, what a replacement would stop — as it named itself.
    """
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "RemoveAction",
]
