# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/repair`, and the shapes only `/api/actions/repair` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class RepairAction(ActionRequest):
    """The action `repair`, with the arguments it is posted with. `agreed`, `confirm` and `offer` carry the operator's yes."""

    ACTION = "repair"

    disruptive: bool
    """Whether the checks that disturb the running system are included."""
    offer: str | None = None
    """What was read before answering — the offer a repair's yes was read in, the
    listing a restore's was, what a replacement would stop — as it named itself.
    """
    agreed: list[str] = dataclasses.field(default_factory=lambda: [])
    """The checks whose repairs were agreed to, as that offer names them."""
    confirm: bool = False
    """Whether a cost the action would incur was agreed to in advance."""
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "RepairAction",
]
