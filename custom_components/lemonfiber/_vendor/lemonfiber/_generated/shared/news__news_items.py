# Copyright (c) 2026 NightWorksIO
"""The shapes `news` and `news-items` both carry.

Generated from `contract/web-api.contract.json`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import typing


type NewsKind = typing.Literal["updates", "requests", "problems"]
"""One of the three kinds of thing a surface can mark as new."""


__all__ = [
    "NewsKind",
]
