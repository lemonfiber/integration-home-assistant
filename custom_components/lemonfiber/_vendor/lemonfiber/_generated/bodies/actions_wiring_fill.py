# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/wiring-fill`, and the shapes only `/api/actions/wiring-fill` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class WiringFillAction(ActionRequest):
    """The action `wiring-fill`, with the arguments it is posted with. `offer` carries the operator's yes."""

    ACTION = "wiring-fill"

    service: str | None = None
    """The one service to act on instead of the whole stack."""
    offer: str | None = None
    """What was read before answering — the offer a repair's yes was read in, the
    listing a restore's was, what a replacement would stop — as it named itself.
    """
    reason: str | None = None
    """Why a request is being turned down, or why a service was chosen to fill a
    capability.
    """
    capability: str | None = None
    """The capability whose filler is being chosen."""
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "WiringFillAction",
]
