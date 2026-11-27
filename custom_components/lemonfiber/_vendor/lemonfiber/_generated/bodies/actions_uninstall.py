# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/uninstall`, and the shapes only `/api/actions/uninstall` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class UninstallAction(ActionRequest):
    """The action `uninstall`, with the arguments it is posted with. `confirm` and `offer` carry the operator's yes."""

    ACTION = "uninstall"

    wait: bool = False
    """Whether anything still downloading is let finish before the stop."""
    offer: str | None = None
    """What was read before answering — the offer a repair's yes was read in, the
    listing a restore's was, what a replacement would stop — as it named itself.
    """
    confirm: bool = False
    """Whether a cost the action would incur was agreed to in advance."""
    tier: str | None = None
    """Which of the four removals an uninstall was asked for.

    A word rather than a level, for the reason `policy` is a word: they are four
    decisions and not a scale, and one this build does not know is refused by
    name rather than falling to whichever removal the shape happened to default
    to — which on this subject would be a library gone.
    """
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "UninstallAction",
]
