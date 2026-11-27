# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/play`, and the shapes only `/api/actions/play` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class PlayAction(ActionRequest):
    """The action `play`, with the arguments it is posted with."""

    ACTION = "play"

    device: str | None = None
    """The id a player keeps for the device it plays on, which a grant opens a session
    for.
    """
    id: str | None = None
    """The thing an action is about, by its id: the title or episode a player's progress
    is on, by the identifier the shelf lists it under, the title a member asks for, by
    the identifier their search listed it under, or the wake a phone confirms.
    """
    pass_: str | None = None
    """The pass a browser holds, handed back for a new one around the same session."""
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "PlayAction",
]
