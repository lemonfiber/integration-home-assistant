# Copyright (c) 2026 NightWorksIO
"""The `held` envelope, and the shapes only `held` carries.

Generated from `contract/web-api.contract.json`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import typing


class Held(typing.TypedDict):
    """One thing the household holds, as a member is shown it.

    What a person recognises and nothing else. There is no file path, no container,
    no bitrate and no library id: a member deciding what to watch is not choosing a
    transcode, and a surface handed those would have to decide not to draw them.
    """

    id: str
    """The identifier the server tells it apart by, which is what asking to play one
    of them names.
    """
    medium: Medium
    """Which of the kinds this product deals in it is."""
    title: str
    """What it is called, in the words the server holds it under."""
    year: typing.NotRequired[int | None]
    """The year it came out, where the server knows one. Absent rather than guessed:
    two films share a title far more often than they share a title and a year.
    """


class HeldEnvelope(typing.TypedDict):
    """The envelope carrying `held`."""

    api_version: int
    data: HeldReport
    host: typing.NotRequired[str | None]
    kind: typing.Literal["held"]


class HeldReport(typing.TypedDict):
    """What one member can watch, and who they are."""

    available: bool
    """Whether the shelf could be read at all.

    An empty shelf and an unread one are different answers, and collapsing them
    would tell a household they own nothing on the day the media server rebooted.
    Anything that could not be read is said in `findings` and this goes false.
    """
    findings: list[str]
    """What is worth saying about this shelf, in the words its reader would use.

    Always written, empty or not. A field the schema requires and the document
    sometimes omits is one a reader has to guess about, and an empty list already
    says the thing it would say: there is nothing to report about this shelf.
    """
    holdings: list[Held]
    """What they hold, newest first."""
    id: str
    """The identifier the media server files them under."""
    member: str
    """The member this was asked for, by the name they are known by."""
    rehearsed: bool
    """Whether this was a rehearsal: what would have happened, with none of it done.

    Said in a field of its own so that a rehearsal is never told from the real run by
    its wording alone.
    """


type Medium = typing.Literal["film", "series", "other"]
"""The kinds of thing a household holds.

Named rather than passed through as the server's own word, because a surface
drawing \"Series\" against one server and \"tvshow\" against another would be
rendering a detail of which server this household runs.

`Medium` rather than `Kind`, `Holding` or `Sort`: this product already calls the two
request services a [`crate::media::Kind`], a request's suspension a
[`crate::service::asking::Holding`], and what one line of a manifest is a
`uninstall::Sort` — and one word meaning two things in one vocabulary is how a
reader comes to trust the wrong one. The contract flattens every type name into one
namespace, so a clash there is a clash for anything reading it by name.
"""


__all__ = [
    "Held",
    "HeldEnvelope",
    "HeldReport",
    "Medium",
]
