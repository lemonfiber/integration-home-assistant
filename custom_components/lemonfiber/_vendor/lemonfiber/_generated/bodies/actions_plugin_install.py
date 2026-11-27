# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/plugin-install`, and the shapes only `/api/actions/plugin-install` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class PluginInstallAction(ActionRequest):
    """The action `plugin-install`, with the arguments it is posted with. `approved` and `offer` carry the operator's yes."""

    ACTION = "plugin-install"

    offer: str | None = None
    """What was read before answering — the offer a repair's yes was read in, the
    listing a restore's was, what a replacement would stop — as it named itself.
    """
    source: str | None = None
    """Where a plugin comes from: its name in the catalogue, its directory on this
    machine or the `plugin.toml` inside it, or a git repository, at a branch, tag or
    commit named after its last `@`.
    """
    approved: list[str] = dataclasses.field(default_factory=lambda: [])
    """Every value a recipe would carry elsewhere that is approved, as `value@destination`,
    every privileged shape, as `shape@service`, and every credential granted to a
    plugin, as `setting@plugin`, exactly as the reading lists them.
    """
    inputs: list[str] = dataclasses.field(default_factory=lambda: [])
    """Every value the operator supplies for an input a recipe asks for, as `name=value`.
    What follows the `=` may be a secret, and is never repeated back.
    """
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "PluginInstallAction",
]
