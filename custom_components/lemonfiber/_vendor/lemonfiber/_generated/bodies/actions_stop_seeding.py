# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/stop-seeding`, and the shapes only `/api/actions/stop-seeding` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class StopSeedingAction(ActionRequest):
    """The action `stop-seeding`, with the arguments it is posted with. `offer` carries the operator's yes."""

    ACTION = "stop-seeding"

    offer: str | None = None
    """What was read before answering — the offer a repair's yes was read in, the
    listing a restore's was, what a replacement would stop — as it named itself.
    """
    download: str | None = None
    """The completed download the client is to be asked to let go, by the name both
    sides use.
    """
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "StopSeedingAction",
]
