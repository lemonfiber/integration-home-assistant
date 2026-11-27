# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/search`, and the shapes only `/api/actions/search` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class SearchAction(ActionRequest):
    """The action `search`, with the arguments it is posted with."""

    ACTION = "search"

    disruptive: bool
    """Whether the checks that disturb the running system are included."""
    term: str | None = None
    """What to follow, named as a person would say it."""
    season: int | None = None
    """The season a followed show is narrowed to, or every season where absent."""


__all__ = [
    "SearchAction",
]
