# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/watched`, and the shapes only `/api/actions/watched` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class WatchedAction(ActionRequest):
    """The action `watched`, with the arguments it is posted with."""

    ACTION = "watched"

    name: str | None = None
    """Who an action addressed to somebody in the household is for, as they sign in."""
    id: str | None = None
    """The thing an action is about, by its id: the title or episode a player's progress
    is on, by the identifier the shelf lists it under, the title a member asks for, by
    the identifier their search listed it under, or the wake a phone confirms.
    """
    position: int | None = None
    """How far into it the member is, in whole seconds."""
    ended: bool | None = None
    """Whether the member finished it. Absent says nothing about finishing, which is
    a position like any other.
    """
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "WatchedAction",
]
