# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/settings-set`, and the shapes only `/api/actions/settings-set` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class SettingsSetAction(ActionRequest):
    """The action `settings-set`, with the arguments it is posted with. `offer` carries the operator's yes."""

    ACTION = "settings-set"

    values: dict[str, str] = dataclasses.field(default_factory=lambda: {})
    """Each setting to change, by the name the settings read lists it under, with the
    value it is to hold, written as exactly itself.
    """
    offer: str | None = None
    """What was read before answering — the offer a repair's yes was read in, the
    listing a restore's was, what a replacement would stop — as it named itself.
    """
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "SettingsSetAction",
]
