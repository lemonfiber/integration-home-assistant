# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/grant`, and the shapes only `/api/actions/grant` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class GrantAction(ActionRequest):
    """The action `grant`, with the arguments it is posted with."""

    ACTION = "grant"

    name: str | None = None
    """Who an action addressed to somebody in the household is for, as they sign in."""
    device: str | None = None
    """The id a player keeps for the device it plays on, which a grant opens a session
    for.
    """
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "GrantAction",
]
