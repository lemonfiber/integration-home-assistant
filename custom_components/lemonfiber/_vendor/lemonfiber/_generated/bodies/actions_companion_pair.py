# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/companion-pair`, and the shapes only `/api/actions/companion-pair` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class CompanionPairAction(ActionRequest):
    """The action `companion-pair`, with the arguments it is posted with."""

    ACTION = "companion-pair"


__all__ = [
    "CompanionPairAction",
]
