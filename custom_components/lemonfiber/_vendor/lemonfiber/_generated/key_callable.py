# Copyright (c) 2026 NightWorksIO
"""Every action an integration key may call, and what the contract says of each.

Generated from `contract/web-api.contract.json`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import types
import typing

type KeyCallableAction = typing.Literal[
    "restart", "diagnose", "update", "downloads-pause", "downloads-resume"
]
"""Every action a key may call; any other is refused to a key, naming its scope."""


class KeyCallable(typing.NamedTuple):
    """What the contract says of one action a key may call."""

    disturbs: bool
    """Whether calling it disturbs the running system."""
    rehearsal: bool
    """Whether it takes `dry_run`, so it can be rehearsed before the real call is offered."""


KEY_CALLABLE: typing.Final[typing.Mapping[KeyCallableAction, KeyCallable]] = types.MappingProxyType(
    {
        "restart": KeyCallable(True, True),
        "diagnose": KeyCallable(True, False),
        "update": KeyCallable(True, True),
        "downloads-pause": KeyCallable(False, True),
        "downloads-resume": KeyCallable(False, True),
    }
)
"""What the contract says of each action a key may call, in the order it lists them."""


def is_key_callable(value: str) -> typing.TypeIs[KeyCallableAction]:
    """Tell whether an action is one the contract says a key may call."""
    return value in KEY_CALLABLE


__all__ = [
    "KEY_CALLABLE",
    "KeyCallable",
    "KeyCallableAction",
    "is_key_callable",
]
