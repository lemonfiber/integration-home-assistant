# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/space`, and the shapes only `/api/actions/space` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class SpaceAction(ActionRequest):
    """The action `space`, with the arguments it is posted with. `offer` carries the operator's yes."""

    ACTION = "space"

    only: list[str] = dataclasses.field(default_factory=lambda: [])
    """The categories of what the offer holds as costing nothing to take, orphaned or extracted; all it holds where none is named."""
    offer: str | None = None
    """What was read before answering — the offer a repair's yes was read in, the
    listing a restore's was, what a replacement would stop — as it named itself.
    """
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "SpaceAction",
]
