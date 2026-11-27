# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/walkthrough`, and the shapes only `/api/actions/walkthrough` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class WalkthroughAction(ActionRequest):
    """The action `walkthrough`, with the arguments it is posted with."""

    ACTION = "walkthrough"

    item: str | None = None
    """The one thing to add end to end, as it would be said."""


__all__ = [
    "WalkthroughAction",
]
