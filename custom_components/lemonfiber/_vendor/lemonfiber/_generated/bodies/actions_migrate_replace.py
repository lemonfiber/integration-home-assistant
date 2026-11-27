# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/migrate-replace`, and the shapes only `/api/actions/migrate-replace` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class MigrateReplaceAction(ActionRequest):
    """The action `migrate-replace`, with the arguments it is posted with. `offer` carries the operator's yes."""

    ACTION = "migrate-replace"

    offer: str | None = None
    """What was read before answering — the offer a repair's yes was read in, the
    listing a restore's was, what a replacement would stop — as it named itself.
    """
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "MigrateReplaceAction",
]
