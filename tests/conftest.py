# Copyright (c) 2026 NightWorksIO
"""The stand-in stack, what it answers with, and an entry that reaches it, shared by every test."""

import asyncio
from typing import TYPE_CHECKING, Any, Final, cast

import pytest
from homeassistant.config_entries import SOURCE_REAUTH
from homeassistant.const import CONF_API_KEY, CONF_URL
from homeassistant.helpers import entity_registry as er
from lemonfiber import KEY_CALLABLE, Read
from lemonfiber.reads import ACTIONS
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.lemonfiber.const import CONF_PIN, DOMAIN
from tests.stack import Feed, Reply, Stack, envelope, event

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Callable

    from homeassistant.config_entries import ConfigFlowResult
    from homeassistant.core import HomeAssistant

KEY: Final = "lfk_" + "a" * 32
VERSION: Final = "0.17.0"
PATIENCE: Final = 10.0
"""Seconds a test waits for the stream or a read to come round: a reopening waits a second first."""
MEMBER_READS: Final = frozenset({Read.REQUESTS, Read.HELD, Read.PLAYING})
"""The reads a member's key reaches: their own row of the household, their own shelf and what they are playing."""


@pytest.fixture(autouse=True)
def custom_integrations(enable_custom_integrations: None) -> None:
    """Let Home Assistant load the integration from `custom_components/`."""


def capabilities(scope: str) -> dict[str, object]:
    """Return what the stack says a key of a scope may ask for: every read, and an action a key may never call."""
    reads = {
        read.path: "unpermitted" if scope == "member" and read not in MEMBER_READS else "available"
        for read in Read
    }
    callable_by_scope = "available" if scope == "act" else "unpermitted"
    actions = {f"{ACTIONS}/{action}": callable_by_scope for action in KEY_CALLABLE}
    return envelope(
        "capabilities",
        {"capabilities": {**reads, **actions, f"{ACTIONS}/repair": "unpermitted"}},
    )


def reading(value: int | None, state: str = "known") -> dict[str, object]:
    """Return a figure a source reports: known or stale with a value, or unknown without one."""
    return {"reading": state} if value is None else {"reading": state, "value": value}


def ready(data: object) -> dict[str, object]:
    """Return a panel whose source answered."""
    return {"panel": "ready", "data": data}


def unavailable(reason: str = "The source did not answer.") -> dict[str, object]:
    """Return a panel whose source could not be reached."""
    return {"panel": "unavailable", "data": {"reason": reason}}


def transfer(speed: dict[str, object]) -> dict[str, object]:
    """Return one active download at a speed."""
    return {"name": "A film", "progress": 40, "protocol": "torrent", "speed": speed}


def service(identifier: str, name: str) -> dict[str, object]:
    """Return one running service as the dashboard names it."""
    return {
        "id": identifier,
        "name": name,
        "state": "running",
        "criticality": "core",
        "depends_on": [],
        "forms": [],
    }


def dashboard(**panels: object) -> dict[str, object]:
    """Return a dashboard as the stack gathers one: healthy, two downloads, a disk and a VPN, with panels replaced."""
    snapshot: dict[str, object] = {
        "alerts": [],
        "door": ready({"address": {"url": "https://127.0.0.1:8096"}, "beside": [], "meaning": "The door."}),
        "health": {"affected": [], "standing": "healthy", "wanting_attention": 0},
        "household": ready({"members": [{"name": "Ana"}]}),
        "queue": ready(
            [{"service": "sonarr", "depth": 3, "stuck": 0}, {"service": "radarr", "depth": 2, "stuck": 1}],
        ),
        "services": ready(
            [service("sonarr", "Sonarr"), service("radarr", "Radarr"), service("jellyfin", "Jellyfin")],
        ),
        "storage": ready({"free": reading(500_000_000_000), "hardlink": "linking"}),
        "stuck": [],
        "telemetry": "live",
        "transfers": ready([transfer(reading(1_500_000)), transfer(reading(500_000))]),
        "vpn": ready({"country": "NL", "egress_matches": True, "exit_ip": "203.0.113.7"}),
    }
    return snapshot | panels


def finding(outcome: str, severity: str | None = None, summary: str = "") -> dict[str, object]:
    """Return one finding of the doctor's, carrying a severity where its verdict is a warning or a failure."""
    verdict: dict[str, object] = {"outcome": outcome}
    if severity is not None:
        verdict |= {"severity": severity, "summary": summary, "meaning": "", "remedies": [], "code": "X-1"}
    return {
        "category": "network",
        "check": f"check.{summary or outcome}",
        "title": summary,
        "verdict": verdict,
    }


def diagnosis(*findings: dict[str, object]) -> dict[str, object]:
    """Return the doctor's report holding these findings."""
    return envelope("doctor", {"findings": list(findings), "overall": "degraded", "rehearsed": False})


DIAGNOSIS: Final = diagnosis(
    finding("pass"),
    finding("warn", "warning", "The disk is filling."),
    finding("fail", "critical", "The tunnel is down."),
    finding("fail", "critical", "Sonarr is not answering."),
    finding("skipped"),
)


PROVENANCE: Final = envelope(
    "provenance",
    {
        "services": [
            {
                "id": "sonarr",
                "name": "Sonarr",
                "image": "x/sonarr",
                "pinned": "4.0.15",
                "license": "GPL-3.0",
                "upstream": "u",
            },
            {
                "id": "radarr",
                "name": "Radarr",
                "image": "x/radarr",
                "pinned": "5.26.2",
                "license": "GPL-3.0",
                "upstream": "u",
            },
        ],
    },
)
"""Where the services come from: two of the dashboard's three, each at the tag this build pins."""

SONARR_STEP: Final[dict[str, object]] = {
    "service": "sonarr",
    "current": "4.0.14",
    "target": "4.0.15",
    "because": "A patch release: fixes, nothing that changes how it is set up.",
    "irreversible": False,
    "jump": "patch",
    "refused": False,
}
"""Sonarr's step, from the tag it stands on to its pin."""


def update(*changes: dict[str, object]) -> dict[str, object]:
    """Return what updating the stack would move: these steps."""
    return envelope(
        "update",
        {
            "applied": [],
            "changes": list(changes),
            "confirmed": False,
            "in_flight": [],
            "rehearsed": False,
            "stack_edits": [],
            "state": "updates-available" if changes else "current",
        },
    )


UPDATE: Final = update(SONARR_STEP)
"""What updating the stack would move: Sonarr, from the tag it stands on to its pin."""


def request(state: str | None, title: str | None = None) -> dict[str, object]:
    """Return one of a member's requests, standing at a state where the service reports one we know, named where it has a title yet."""
    asked: dict[str, object] = {"id": 7}
    if state is not None:
        asked["state"] = state
    if title is not None:
        asked["title"] = title
    return asked


def household(*requests: dict[str, object], available: bool = True) -> dict[str, object]:
    """Return a member's row of the household as their stream says it: Ana, and what she asked for."""
    row: dict[str, object] = {
        "access": {
            "administrator": False,
            "disabled": False,
            "every_library": True,
            "libraries": [],
            "restriction": "unrestricted",
            "unrated": "let-through",
        },
        "claimed": True,
        "name": "Ana",
        "requests": list(requests),
        "standing": "active",
        "to_hand_over": [],
    }
    return {"available": available, "findings": [], "members": [row] if available else [], "rehearsed": False}


HOUSEHOLD: Final = household(
    request("waiting-for-approval"),
    request("getting", "Dune: Part Two"),
    request("getting", "Severance"),
    request("here", "Paddington in Peru"),
    request(None, "A title in a state this build does not know"),
)
"""Ana's row: one request waiting, two on their way, one here, and one in a state nobody knows."""


def playback(*, paused: bool = False) -> dict[str, object]:
    """Return Ana watching an episode on the living room television."""
    return {
        "device": "Living room TV",
        "episode": 3,
        "medium": "series",
        "member": "Ana",
        "member_id": "a1",
        "paused": paused,
        "season": 2,
        "series": "Severance",
        "title": "Who Is Alive?",
    }


def playing(*sessions: dict[str, object], available: bool = True) -> dict[str, object]:
    """Return what a member is playing, as their stream says it."""
    return {"available": available, "findings": [], "member": "Ana", "sessions": list(sessions)}


def serve(stack: Stack, scope: str = "read", *feeds: Feed) -> Feed:
    """Have the stand-in answer as a stack does for a key of a scope, its stream opening as each feed in turn.

    A member's stream opens with their household row and what they are playing;
    every other opens with the dashboard.
    """
    stack.reply("/api/capabilities", Reply(body=capabilities(scope)))
    stack.reply("/api/version", Reply(body=envelope("version", {"binary": VERSION, "stack": "1"})))
    stack.reply("/api/checks", Reply(body=DIAGNOSIS))
    stack.reply("/api/provenance", Reply(body=PROVENANCE))
    stack.reply("/api/update", Reply(body=UPDATE))
    opened = feeds or (Feed(),)
    if scope == "member":
        opened[0].say(event("household", HOUSEHOLD, "1"), event("playing", playing(), "2"))
    else:
        opened[0].say(event("dashboard", dashboard(), "1"))
    stack.stream(*opened)
    return opened[0]


@pytest.fixture
async def stack(hass: HomeAssistant, socket_enabled: None) -> AsyncIterator[Stack]:
    """Serve TLS on loopback, with a certificate no trust store holds and a pin that names it.

    Home Assistant's test harness refuses every socket until a test asks for them,
    and still lets them reach loopback alone. It is started once Home Assistant
    is, on the same event loop.
    """
    async with Stack() as serving:
        yield serving


def entry_for(stack: Stack, unique_id: str | None = None) -> MockConfigEntry:
    """Return an entry holding the stand-in's address, pin and a key, identified by the address unless told otherwise."""
    return MockConfigEntry(
        domain=DOMAIN,
        title="127.0.0.1",
        unique_id=unique_id or stack.url,
        data={CONF_URL: stack.url, CONF_API_KEY: KEY, CONF_PIN: stack.pin},
    )


@pytest.fixture
def entry(hass: HomeAssistant, stack: Stack) -> MockConfigEntry:
    """Add an entry for the stand-in to Home Assistant, not yet set up."""
    added = entry_for(stack)
    added.add_to_hass(hass)
    return added


def enabled(hass: HomeAssistant, entry: MockConfigEntry, entity_id: str, key: str) -> None:
    """Register an entity left off by default as enabled, before the entry is set up, under the id it would get."""
    domain, object_id = entity_id.split(".")
    er.async_get(hass).async_get_or_create(
        domain,
        DOMAIN,
        f"{entry.entry_id}-{key}",
        config_entry=entry,
        suggested_object_id=object_id,
    )


async def until(hass: HomeAssistant, done: Callable[[], bool]) -> None:
    """Wait until something is true, as the stream, the reads and the stand-in move Home Assistant there."""
    async with asyncio.timeout(PATIENCE):
        while not done():
            await asyncio.sleep(0.05)
            await hass.async_block_till_done()


def said(result: ConfigFlowResult) -> dict[str, Any]:
    """Return what a flow answered, each field read as whatever it holds."""
    return cast("dict[str, Any]", result)


def reauthenticating(hass: HomeAssistant) -> bool:
    """Tell whether Home Assistant has asked for a new key."""
    return any(
        said(flow).get("context", {}).get("source") == SOURCE_REAUTH
        for flow in hass.config_entries.flow.async_progress()
    )
