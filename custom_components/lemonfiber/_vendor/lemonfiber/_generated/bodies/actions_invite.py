# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/invite`, and the shapes only `/api/actions/invite` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class InviteAction(ActionRequest):
    """The action `invite`, with the arguments it is posted with. `confirm` carries the operator's yes."""

    ACTION = "invite"

    name: str | None = None
    """Who an action addressed to somebody in the household is for, as they sign in."""
    libraries: list[str] = dataclasses.field(default_factory=lambda: [])
    """The libraries an invitation lets them open, by the names the media server
    gives those libraries. Empty is every one.
    """
    age_limit: int | None = None
    """The age above which an invitation has the media server hold things back."""
    unrated: str | None = None
    """What is to happen to content the media server has no rating for.

    A word rather than a switch, because the choice has a cost either way and a
    switch has a default nobody can see: `block` holds unrated content back, and
    `allow` lets it through. Carried as it was written and read next door, so a
    word this build does not know is refused by name rather than falling to
    whichever answer the shape happened to default to.
    """
    confirm: bool = False
    """Whether a cost the action would incur was agreed to in advance."""
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "InviteAction",
]
