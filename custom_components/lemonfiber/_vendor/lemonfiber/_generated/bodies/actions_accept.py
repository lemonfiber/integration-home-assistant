# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/accept`, and the shapes only `/api/actions/accept` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class AcceptAction(ActionRequest):
    """The action `accept`, with the arguments it is posted with."""

    ACTION = "accept"

    check: str | None = None
    """The check a warning is being answered for."""
    disruptive: bool
    """Whether the checks that disturb the running system are included."""


__all__ = [
    "AcceptAction",
]
