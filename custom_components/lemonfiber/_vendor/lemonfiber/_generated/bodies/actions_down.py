# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/down`, and the shapes only `/api/actions/down` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class DownAction(ActionRequest):
    """The action `down`, with the arguments it is posted with."""

    ACTION = "down"

    forms: list[str] = dataclasses.field(default_factory=lambda: [])
    """The forms to act on."""
    services: list[str] = dataclasses.field(default_factory=lambda: [])
    """The services to act on, leaving the rest of the form alone."""
    wait: bool = False
    """Whether anything still downloading is let finish before the stop."""
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "DownAction",
]
