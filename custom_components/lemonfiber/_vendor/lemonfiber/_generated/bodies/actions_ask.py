# Copyright (c) 2026 NightWorksIO
"""The action posted to `/api/actions/ask`, and the shapes only `/api/actions/ask` carries.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses

from ..actions import ActionRequest


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class AskAction(ActionRequest):
    """The action `ask`, with the arguments it is posted with."""

    ACTION = "ask"

    name: str | None = None
    """Who an action addressed to somebody in the household is for, as they sign in."""
    id: str | None = None
    """The thing an action is about, by its id: the title or episode a player's progress
    is on, by the identifier the shelf lists it under, the title a member asks for, by
    the identifier their search listed it under, or the wake a phone confirms.
    """
    kind: str | None = None
    """Whether the title asked for is a series, a film, music or books, as a page of a
    member's search names it: `tv`, `movies`, `music` or `books`.
    """
    seasons: list[int] = dataclasses.field(default_factory=lambda: [])
    """The seasons of a series asked for. None names every season not already here or
    on its way.
    """
    unit: str | None = None
    """What is asked for within music or books, as a page of a member's search names
    it: `album` or `artist`, `book`, `author` or `series`. Absent asks for an album
    or a book.
    """
    found: str | None = None
    """The token a page of a member's search vouched for the title asked for with, handed
    back as the page gave it.
    """
    dry_run: bool = False
    """Whether to rehearse: write nothing, and answer with what the action would do."""


__all__ = [
    "AskAction",
]
