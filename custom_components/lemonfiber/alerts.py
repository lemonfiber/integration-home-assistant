# Copyright (c) 2026 NightWorksIO
"""Each alert the stream carries, fired as a `lemonfiber_alert` event at its onset and at its resolution.

The event carries what the stack said and nothing the entry holds: what
happened, what it means, what to do, how much it matters and which way it went,
with the identity an onset shares with the resolution that ends it.
"""

from typing import TYPE_CHECKING, Final

from lemonfiber import Live, expect

from .const import DOMAIN

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from lemonfiber import Arrival
    from lemonfiber.contract import Alert

    from .runtime import LemonfiberConfigEntry

ALERT: Final = "alert"
"""The kind the stream carries an alert in."""

ALERT_EVENT: Final = f"{DOMAIN}_alert"
"""The event every alert is fired as."""


def alert_in(arrival: Arrival) -> Alert | None:
    """Return the alert an arrival carries live, or None where it is anything else."""
    if not isinstance(arrival, Live) or arrival.envelope["kind"] != ALERT:
        return None
    return expect(arrival.envelope, ALERT)["data"]


def told(alert: Alert) -> dict[str, object]:
    """Return an alert in the stack's own words: what happened, what it means, what to do, and which way it went."""
    carried: dict[str, object] = {
        "moment": alert["moment"],
        "severity": alert["severity"],
        "kind": alert["kind"],
        "check": alert["check"],
        "affected": list(alert["affected"]),
        "summary": alert["summary"],
        "meaning": alert["meaning"],
        "remedies": list(alert["remedies"]),
    }
    if (identity := alert.get("id")) is not None:
        carried["id"] = identity
    if (exited := alert.get("exit")) is not None:
        carried["exit"] = exited
    return carried


def fire(hass: HomeAssistant, entry: LemonfiberConfigEntry, alert: Alert) -> None:
    """Fire an alert as the entry's event."""
    hass.bus.async_fire(ALERT_EVENT, {"entry_id": entry.entry_id, **told(alert)})
