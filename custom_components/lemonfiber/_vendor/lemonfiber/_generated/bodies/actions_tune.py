# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/tune`, and the shapes only `/api/actions/tune` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class TuneAction(ActionRequest):
    """The action `tune`, with the arguments it is posted with."""

    ACTION = "tune"

    id: str | None = None
    """The thing an action is about, by its id: the title or episode a player's progress
    is on, by the identifier the shelf lists it under, the title a member asks for, by
    the identifier their search listed it under, or the wake a phone confirms.
    """
    stream: str | None = None
    """The live stream a renewal or a stop names, as a channel opened for the member
    answered it.
    """
    stop: bool | None = None
    """Whether to close the live stream named rather than renew its passes."""
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "TuneAction",
]
