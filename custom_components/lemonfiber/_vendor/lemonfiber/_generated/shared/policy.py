# Copyright (c) 2026 NightWorksIO
"""The shapes `askable`, `dashboard`, `household` and `invitation` all carry.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import typing


type Policy = typing.Literal["trusted", "within-a-limit", "everything-waits"]
"""What happens to what a household member asks for.

Three, and they are the three the request service can actually be put into. A
household is in one of them because of two settings taken together — whether requests
arrive unseen, and whether a period limits how many — so the words here are a reading
of that pair rather than a fourth setting kept beside it.

Choosing per person is not a fourth policy. It is one of these three chosen for one
member rather than for the house, which is why what a surface offers is a policy and,
separately, who it is for.
"""


__all__ = [
    "Policy",
]
