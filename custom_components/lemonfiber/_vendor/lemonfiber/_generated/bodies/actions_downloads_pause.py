# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/downloads-pause`, and the shapes only `/api/actions/downloads-pause` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class DownloadsPauseAction(ActionRequest):
    """The action `downloads-pause`, with the arguments it is posted with. `offer` carries the operator's yes."""

    ACTION = "downloads-pause"

    offer: str | None = None
    """What was read before answering — the offer a repair's yes was read in, the
    listing a restore's was, what a replacement would stop — as it named itself.
    """
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "DownloadsPauseAction",
]
