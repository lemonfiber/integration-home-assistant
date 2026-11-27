# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/quality-set`, and the shapes only `/api/actions/quality-set` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class QualitySetAction(ActionRequest):
    """The action `quality-set`, with the arguments it is posted with. `confirm` carries the operator's yes."""

    ACTION = "quality-set"

    preset: str | None = None
    """The quality preset, or the music format, as it is written."""
    media_type: str | None = None
    """The media type a quality choice applies to."""
    confirm: bool = False
    """Whether a cost the action would incur was agreed to in advance."""
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "QualitySetAction",
]
