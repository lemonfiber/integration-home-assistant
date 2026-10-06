# Copyright (c) 2026 NightWorksIO
"""The `word` envelope, and the shapes only `word` carries.

Generated from `contract/web-api.contract.json`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import typing

from ..shared.glossary__word import Term


class WordEnvelope(typing.TypedDict):
    """The envelope carrying `word`."""

    api_version: int
    data: Term
    host: typing.NotRequired[str | None]
    kind: typing.Literal["word"]


__all__ = [
    "WordEnvelope",
]
