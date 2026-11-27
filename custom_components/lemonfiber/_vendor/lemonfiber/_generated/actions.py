# Copyright (c) 2026 NightWorksIO
"""Every action the web API takes, what the contract says of each, and what each request is.

Generated from the contract vendored in `contract/`. Do not edit: `just generate` rewrites it,
and CI fails on any difference.
"""

import dataclasses
import types
import typing

type ActionName = typing.Literal[
    "accept",
    "adopt",
    "ask",
    "backup",
    "bandwidth",
    "companion-pair",
    "config-set",
    "credentials-revoke",
    "diagnose",
    "down",
    "downloads-pause",
    "downloads-resume",
    "forget",
    "grant",
    "hosting-install",
    "hosting-remove",
    "household-allow",
    "household-approve",
    "household-decline",
    "household-handoff",
    "internal-certificate-replace",
    "invite",
    "migrate-adopt",
    "migrate-beside",
    "migrate-import",
    "migrate-replace",
    "notify-choose",
    "play",
    "plugin-install",
    "plugin-prove",
    "plugin-remove",
    "plugin-run",
    "plugin-update",
    "pull",
    "push-woken",
    "quality-reapply",
    "quality-set",
    "quality-upgrade",
    "reissue",
    "remove",
    "repair",
    "reset",
    "restart",
    "restore",
    "run",
    "search",
    "seed",
    "settings-clear",
    "settings-set",
    "space",
    "stop-seeding",
    "support",
    "switch",
    "tune",
    "undo",
    "uninstall",
    "up",
    "update",
    "walkthrough",
    "watch",
    "watched",
    "wiring-fill",
]
"""Every action the web API takes, by the name it is posted to under `/api/actions/`."""


class ActionDescribed(typing.NamedTuple):
    """What the contract says of one action."""

    arguments: tuple[str, ...]
    """The name of every argument it takes, in the order the contract lists them."""
    consent: tuple[str, ...]
    """The arguments carrying the operator's yes, without which it writes nothing."""
    rehearsal: bool
    """Whether it takes `dry_run`, so it can be rehearsed before the real call."""


ACTIONS: typing.Final[typing.Mapping[ActionName, ActionDescribed]] = types.MappingProxyType(
    {
        "accept": ActionDescribed(("check", "disruptive"), (), False),
        "adopt": ActionDescribed((), (), True),
        "ask": ActionDescribed(("name", "id", "kind", "seasons", "unit", "found"), (), True),
        "backup": ActionDescribed(("service",), (), True),
        "bandwidth": ActionDescribed(
            ("down", "up", "active", "line", "cap", "exceeded", "unrestricted_for"), (), True
        ),
        "companion-pair": ActionDescribed((), (), False),
        "config-set": ActionDescribed(("wait", "key", "value", "confirm"), ("confirm",), True),
        "credentials-revoke": ActionDescribed(("offer", "plugin", "credential"), ("offer",), True),
        "diagnose": ActionDescribed(("only", "disruptive"), (), False),
        "down": ActionDescribed(("forms", "services", "wait"), (), True),
        "downloads-pause": ActionDescribed(("offer",), ("offer",), True),
        "downloads-resume": ActionDescribed(("offer",), ("offer",), True),
        "forget": ActionDescribed(("confirm",), ("confirm",), True),
        "grant": ActionDescribed(("name", "device"), (), True),
        "hosting-install": ActionDescribed(("forms", "kept"), (), True),
        "hosting-remove": ActionDescribed(("kept",), (), True),
        "household-allow": ActionDescribed(("name", "policy", "requests", "days"), (), True),
        "household-approve": ActionDescribed(("request",), (), True),
        "household-decline": ActionDescribed(("request", "reason"), (), True),
        "household-handoff": ActionDescribed(("name",), (), True),
        "internal-certificate-replace": ActionDescribed(("offer",), ("offer",), True),
        "invite": ActionDescribed(
            ("name", "libraries", "age_limit", "unrated", "confirm"), ("confirm",), True
        ),
        "migrate-adopt": ActionDescribed(("confirm",), ("confirm",), True),
        "migrate-beside": ActionDescribed(("confirm",), ("confirm",), True),
        "migrate-import": ActionDescribed(("confirm",), ("confirm",), True),
        "migrate-replace": ActionDescribed(("offer",), ("offer",), True),
        "notify-choose": ActionDescribed(("backends",), (), True),
        "play": ActionDescribed(("device", "id", "pass"), (), True),
        "plugin-install": ActionDescribed(
            ("offer", "source", "approved", "inputs"), ("offer", "approved"), True
        ),
        "plugin-prove": ActionDescribed(("offer", "plugin"), ("offer",), True),
        "plugin-remove": ActionDescribed(("offer", "plugin"), ("offer",), True),
        "plugin-run": ActionDescribed(
            ("offer", "plugin", "recipe", "approved", "inputs"), ("offer", "approved"), True
        ),
        "plugin-update": ActionDescribed(
            ("offer", "plugin", "source", "approved", "inputs"), ("offer", "approved"), True
        ),
        "pull": ActionDescribed(("forms",), (), True),
        "push-woken": ActionDescribed(("name", "id"), (), True),
        "quality-reapply": ActionDescribed((), (), True),
        "quality-set": ActionDescribed(("preset", "media_type", "confirm"), ("confirm",), True),
        "quality-upgrade": ActionDescribed(("confirm",), ("confirm",), True),
        "reissue": ActionDescribed(("name",), (), True),
        "remove": ActionDescribed(("name", "offer"), ("offer",), True),
        "repair": ActionDescribed(
            ("disruptive", "offer", "agreed", "confirm"), ("offer", "agreed", "confirm"), True
        ),
        "reset": ActionDescribed(("offer",), ("offer",), True),
        "restart": ActionDescribed(("forms", "services", "offer"), ("offer",), True),
        "restore": ActionDescribed(("archive", "repoint", "offer", "confirm"), ("offer", "confirm"), True),
        "run": ActionDescribed(("service", "now"), (), True),
        "search": ActionDescribed(("disruptive", "term", "season"), (), False),
        "seed": ActionDescribed((), (), True),
        "settings-clear": ActionDescribed(("settings", "offer"), ("offer",), True),
        "settings-set": ActionDescribed(("values", "offer"), ("offer",), True),
        "space": ActionDescribed(("only", "offer"), ("offer",), True),
        "stop-seeding": ActionDescribed(("offer", "download"), ("offer",), True),
        "support": ActionDescribed(("write", "logs", "filenames", "reveal", "confirm"), ("confirm",), True),
        "switch": ActionDescribed(("forms", "offer"), ("offer",), True),
        "tune": ActionDescribed(("id", "stream", "stop"), (), True),
        "undo": ActionDescribed(("at",), (), True),
        "uninstall": ActionDescribed(("wait", "offer", "confirm", "tier"), ("offer", "confirm"), True),
        "up": ActionDescribed(("forms", "services", "offer"), ("offer",), True),
        "update": ActionDescribed(("wait", "service", "offer", "confirm"), ("offer", "confirm"), True),
        "walkthrough": ActionDescribed(("item",), (), False),
        "watch": ActionDescribed(("forms",), (), True),
        "watched": ActionDescribed(("name", "id", "position", "ended"), (), True),
        "wiring-fill": ActionDescribed(("service", "offer", "reason", "capability"), ("offer",), True),
    }
)
"""What the contract says of every action the web API takes, by name."""


def is_action_name(value: str) -> typing.TypeIs[ActionName]:
    """Tell whether a name is one of an action the web API takes."""
    return value in ACTIONS


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class ActionRequest:
    """One action the web API takes, with the arguments it is posted with."""

    ACTION: typing.ClassVar[ActionName]
    """The name it is posted to under `/api/actions/`."""

    def arguments(self) -> dict[str, object]:
        """Return the arguments it is posted with, each under the name the contract gives it.

        An argument Python reserves the name of is a field spelled with a trailing underscore,
        as `pass_` is posted as `pass`.
        """
        return {one.name.removesuffix("_"): getattr(self, one.name) for one in dataclasses.fields(self)}


__all__ = [
    "ACTIONS",
    "ActionDescribed",
    "ActionName",
    "ActionRequest",
    "is_action_name",
]
