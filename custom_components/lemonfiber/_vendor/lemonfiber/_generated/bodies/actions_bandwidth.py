# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/bandwidth`, and the shapes only `/api/actions/bandwidth` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class BandwidthAction(ActionRequest):
    """The action `bandwidth`, with the arguments it is posted with."""

    ACTION = "bandwidth"

    down: str | None = None
    """How much of the line downloads may take, as a share or a rate.

    Carried as it was written and read in the core, like `unrated` above and for
    the same reason: a surface that decided what `50%` meant would be a second
    answer to the question, and the two would part company on the first change
    to either — which a household would meet as an evening that went wrong on
    one surface and not on another.
    """
    up: str | None = None
    """How much of it uploads may take, set apart from the download."""
    active: str | None = None
    """The hours the household is awake, as `HH:MM-HH:MM` on the wall clock."""
    line: str | None = None
    """What the line carries, as `<down>/<up>`, where the operator knows."""
    cap: str | None = None
    """A monthly allowance for what the stack itself moves."""
    exceeded: str | None = None
    """What is to happen when that cap is reached, decided in advance."""
    unrestricted_for: int | None = None
    """How many minutes to lift the limits for, and no longer."""
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "BandwidthAction",
]
