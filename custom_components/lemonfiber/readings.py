# Copyright (c) 2026 NightWorksIO
"""What each entity reads from the dashboard and the doctor's report, or None where the stack cannot say.

The stack keeps a figure it could not read this time apart from one it read as
zero: a panel whose source did not answer is `unavailable`, and a reading is
`known`, `stale` or `unknown`. Only a panel that is `ready` and a reading that is
`known` is current, so anything else is unavailable here rather than shown as a
value.
"""

import typing
from typing import TYPE_CHECKING, Final

from lemonfiber.contract import HealthStanding, ProblemSeverity

if TYPE_CHECKING:
    from lemonfiber.contract import DashboardReading, DoctorReport, Snapshot

READY: Final = "ready"
"""A panel whose source answered."""
KNOWN: Final = "known"
"""A reading the source gave this time."""
UNKNOWN: Final = "unknown"
"""The standing of a stack nothing could be said about."""

STANDINGS: Final[tuple[HealthStanding, ...]] = tuple(
    standing for standing in typing.get_args(HealthStanding.__value__) if standing != UNKNOWN
)
"""Every standing a stack can be shown in, best first. `unknown` is shown as unavailable."""

SEVERITIES: Final[tuple[ProblemSeverity, ...]] = typing.get_args(ProblemSeverity.__value__)
"""Every severity a finding can carry, least first."""


def known(reading: DashboardReading) -> int | None:
    """Return a reading's value where the source gave it this time."""
    return reading["value"] if reading["reading"] == KNOWN else None


def health(snapshot: Snapshot) -> HealthStanding | None:
    """Return the stack's standing, the one word every surface grades it with."""
    standing = snapshot["health"]["standing"]
    return None if standing == UNKNOWN else standing


def wanting_attention(snapshot: Snapshot) -> bool | None:
    """Return whether anything is wrong, by the stack's own count of what is."""
    if health(snapshot) is None:
        return None
    return snapshot["health"]["wanting_attention"] > 0


def worst(snapshot: Snapshot) -> dict[str, str]:
    """Return the worst thing wrong, named, where anything is."""
    named = snapshot["health"].get("worst")
    return {} if named is None else {"worst": named}


def queued(snapshot: Snapshot) -> int | None:
    """Return how many items wait in every queue together."""
    panel = snapshot["queue"]
    if panel["panel"] != READY:
        return None
    return sum(queue["depth"] for queue in panel["data"])


def speed(snapshot: Snapshot) -> int | None:
    """Return the bytes per second every active download comes to, where each one's speed is current."""
    panel = snapshot["transfers"]
    if panel["panel"] != READY:
        return None
    total = 0
    for transfer in panel["data"]:
        reading = known(transfer["speed"])
        if reading is None:
            return None
        total += reading
    return total


def disk_free(snapshot: Snapshot) -> int | None:
    """Return the bytes free on the data volume."""
    panel = snapshot["storage"]
    if panel["panel"] != READY:
        return None
    return known(panel["data"]["free"])


def has_vpn(snapshot: Snapshot) -> bool:
    """Tell whether the stack has a VPN to report on at all."""
    return snapshot.get("vpn") is not None


def vpn_up(snapshot: Snapshot) -> bool | None:
    """Return whether the download client's traffic leaves through the tunnel."""
    panel = snapshot.get("vpn")
    if panel is None or panel["panel"] != READY:
        return None
    return panel["data"]["egress_matches"]


def findings(report: DoctorReport, severity: ProblemSeverity) -> list[str]:
    """Return what each finding of a severity says happened, in the order the checks produced them."""
    said: list[str] = []
    for finding in report["findings"]:
        verdict = finding["verdict"]
        if (verdict["outcome"] == "fail" or verdict["outcome"] == "warn") and verdict["severity"] == severity:
            said.append(verdict["summary"])
    return said
