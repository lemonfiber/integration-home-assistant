# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/update`, and the shapes only `/api/actions/update` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class UpdateAction(ActionRequest):
    """The action `update`, with the arguments it is posted with. `confirm` and `offer` carry the operator's yes."""

    ACTION = "update"

    wait: bool = False
    """Whether anything still downloading is let finish before the stop."""
    service: str | None = None
    """The one service to act on instead of the whole stack."""
    offer: str | None = None
    """What was read before answering — the offer a repair's yes was read in, the
    listing a restore's was, what a replacement would stop — as it named itself.
    """
    confirm: bool = False
    """Whether a cost the action would incur was agreed to in advance."""
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "UpdateAction",
]
