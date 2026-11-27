# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/plugin-run`, and the shapes only `/api/actions/plugin-run` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class PluginRunAction(ActionRequest):
    """The action `plugin-run`, with the arguments it is posted with. `approved` and `offer` carry the operator's yes."""

    ACTION = "plugin-run"

    offer: str | None = None
    """What was read before answering — the offer a repair's yes was read in, the
    listing a restore's was, what a replacement would stop — as it named itself.
    """
    plugin: str | None = None
    """The plugin an update or a removal acts on, by the id the record of what is
    installed lists it under.
    """
    recipe: str | None = None
    """The demand recipe a run asks for, by the id the plugin's reading lists it under."""
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
    "PluginRunAction",
]
