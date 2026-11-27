# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/notify-choose`, and the shapes only `/api/actions/notify-choose` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class NotifyChooseAction(ActionRequest):
    """The action `notify-choose`, with the arguments it is posted with."""

    ACTION = "notify-choose"

    backends: list[str] = dataclasses.field(default_factory=lambda: [])
    """Each way to be told a member chooses, by the id the operator's offer lists it under."""
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "NotifyChooseAction",
]
