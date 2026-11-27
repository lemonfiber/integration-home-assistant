# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/household-allow`, and the shapes only `/api/actions/household-allow` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class HouseholdAllowAction(ActionRequest):
    """The action `household-allow`, with the arguments it is posted with."""

    ACTION = "household-allow"

    name: str | None = None
    """Who an action addressed to somebody in the household is for, as they sign in."""
    policy: str | None = None
    """What is to happen to what the household asks for, as it is written.

    A word rather than a switch, for the reason `unrated` is one: there are three
    answers rather than two, and a word this build does not know is refused by name
    instead of falling to whichever arrangement the shape happened to default to.
    """
    requests: int | None = None
    """How many requests a period allows."""
    days: int | None = None
    """How long that period is, in days."""
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "HouseholdAllowAction",
]
