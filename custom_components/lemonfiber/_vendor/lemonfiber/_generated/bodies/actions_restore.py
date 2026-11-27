# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/restore`, and the shapes only `/api/actions/restore` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class RestoreAction(ActionRequest):
    """The action `restore`, with the arguments it is posted with. `confirm` and `offer` carry the operator's yes."""

    ACTION = "restore"

    archive: str | None = None
    """The backup to restore from, by the name it was written under."""
    repoint: bool = False
    """Whether re-pointing to this machine's data root was accepted."""
    offer: str | None = None
    """What was read before answering — the offer a repair's yes was read in, the
    listing a restore's was, what a replacement would stop — as it named itself.
    """
    confirm: bool = False
    """Whether a cost the action would incur was agreed to in advance."""
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "RestoreAction",
]
