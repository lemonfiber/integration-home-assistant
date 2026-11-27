# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/config-set`, and the shapes only `/api/actions/config-set` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class ConfigSetAction(ActionRequest):
    """The action `config-set`, with the arguments it is posted with. `confirm` carries the operator's yes."""

    ACTION = "config-set"

    wait: bool = False
    """Whether anything still downloading is let finish before the stop."""
    key: str | None = None
    """The configuration key to change."""
    value: str | None = None
    """What to change the key to, written as exactly itself."""
    confirm: bool = False
    """Whether a cost the action would incur was agreed to in advance."""
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "ConfigSetAction",
]
