# Copyright (c) 2026 NightWorksIO
"""Every rule of Home Assistant's quality scale through Platinum has a status, and every exemption a reason."""

import pathlib
from typing import Final, cast

import pytest
import yaml

SCALE: Final = (
    pathlib.Path(__file__).resolve().parent.parent / "custom_components" / "lemonfiber" / "quality_scale.yaml"
)
RULES: Final = frozenset(
    {
        # Bronze, as Home Assistant 2026.9's hassfest lists the rules.
        "action-setup", "appropriate-polling", "brands", "common-modules", "config-flow",
        "config-flow-test-coverage", "dependency-transparency", "docs-actions", "docs-conditions",
        "docs-high-level-description", "docs-installation-instructions", "docs-removal-instructions",
        "docs-triggers", "entity-event-setup", "entity-unique-id", "has-entity-name", "runtime-data",
        "test-before-configure", "test-before-setup", "unique-config-entry",
        # Silver
        "action-exceptions", "config-entry-unloading", "docs-configuration-parameters",
        "docs-installation-parameters", "entity-unavailable", "integration-owner", "log-when-unavailable",
        "parallel-updates", "reauthentication-flow", "test-coverage",
        # Gold
        "devices", "diagnostics", "discovery", "discovery-update-info", "docs-data-update", "docs-examples",
        "docs-known-limitations", "docs-supported-devices", "docs-supported-functions", "docs-troubleshooting",
        "docs-use-cases", "dynamic-devices", "entity-category", "entity-device-class",
        "entity-disabled-by-default", "entity-translations", "exception-translations", "icon-translations",
        "reconfiguration-flow", "repair-issues", "stale-devices",
        # Platinum
        "async-dependency", "inject-websession", "strict-typing",
    },
)  # fmt: skip
STATUSES: Final = frozenset({"done", "exempt", "todo"})


def tracked() -> dict[str, object]:
    """Return every rule the file tracks, with its status."""
    return cast("dict[str, dict[str, object]]", yaml.safe_load(SCALE.read_text(encoding="utf-8")))["rules"]


def test_every_rule_through_platinum_is_tracked_and_nothing_else() -> None:
    assert tracked().keys() == RULES


@pytest.mark.parametrize("rule", sorted(RULES))
def test_every_rule_has_a_status_and_every_exemption_a_reason(rule: str) -> None:
    held = tracked()[rule]
    if isinstance(held, str):
        assert held in STATUSES - {"exempt"}
        return
    entry = cast("dict[str, str]", held)
    assert entry["status"] in STATUSES
    assert entry["status"] != "exempt" or entry["comment"].strip()
