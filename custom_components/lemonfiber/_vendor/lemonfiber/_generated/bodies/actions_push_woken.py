# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/push-woken`, and the shapes only `/api/actions/push-woken` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class PushWokenAction(ActionRequest):
    """The action `push-woken`, with the arguments it is posted with."""

    ACTION = "push-woken"

    name: str | None = None
    """Who an action addressed to somebody in the household is for, as they sign in."""
    id: str | None = None
    """The thing an action is about, by its id: the title or episode a player's progress
    is on, by the identifier the shelf lists it under, the title a member asks for, by
    the identifier their search listed it under, or the wake a phone confirms.
    """
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "PushWokenAction",
]
