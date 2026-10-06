# Copyright (c) 2026 NightWorksIO
"""The shapes `lifecycle` and `status` both carry.

Generated from `contract/web-api.contract.json`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import typing


type Condition = typing.Literal["inactive", "degraded", "partial", "active"]
"""What a whole set of services amounts to."""


__all__ = [
    "Condition",
]
