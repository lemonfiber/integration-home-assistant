# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/support`, and the shapes only `/api/actions/support` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class SupportAction(ActionRequest):
    """The action `support`, with the arguments it is posted with. `confirm` carries the operator's yes."""

    ACTION = "support"

    write: bool = False
    """Whether to produce the bundle, rather than say what one would hold."""
    logs: int | None = None
    """How many log lines to take from each service."""
    filenames: bool = False
    """Whether media filenames are shown rather than replaced."""
    reveal: list[str] = dataclasses.field(default_factory=lambda: [])
    """The settings to show as they are, named as the bundle names them."""
    confirm: bool = False
    """Whether a cost the action would incur was agreed to in advance."""
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "SupportAction",
]
