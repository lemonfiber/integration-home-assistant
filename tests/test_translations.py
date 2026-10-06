# Copyright (c) 2026 NightWorksIO
"""Every string the integration shows, in English and in Dutch, and every reason and standing with its words."""

import json
import pathlib
import re
from typing import Final, cast

import pytest

from custom_components.lemonfiber.binary_sensor import DASHBOARD_BINARY_SENSORS
from custom_components.lemonfiber.connection import Reason
from custom_components.lemonfiber.readings import SEVERITIES, STANDINGS
from custom_components.lemonfiber.sensor import DASHBOARD_SENSORS, FINDINGS_SENSORS

INTEGRATION: Final = pathlib.Path(__file__).resolve().parent.parent / "custom_components" / "lemonfiber"
PLACEHOLDER: Final = re.compile(r"\{(\w+)\}")


def load(name: str) -> dict[str, object]:
    """Return one of the integration's string files."""
    return json.loads((INTEGRATION / name).read_text(encoding="utf-8"))


def leaves(tree: object, path: str = "") -> dict[str, str]:
    """Return every string in a tree of them, by its dotted path."""
    if isinstance(tree, dict):
        found: dict[str, str] = {}
        for name, branch in cast("dict[str, object]", tree).items():
            found |= leaves(branch, f"{path}.{name}" if path else name)
        return found
    assert isinstance(tree, str), path
    return {path: tree}


ENGLISH: Final = leaves(load("strings.json"))


def test_the_english_translation_is_the_strings_file() -> None:
    assert load("translations/en.json") == load("strings.json")


@pytest.mark.parametrize("language", ["nl"])
def test_every_string_is_translated_with_the_same_placeholders(language: str) -> None:
    translated = leaves(load(f"translations/{language}.json"))
    assert translated.keys() == ENGLISH.keys()
    for path, said in ENGLISH.items():
        assert set(PLACEHOLDER.findall(translated[path])) == set(PLACEHOLDER.findall(said)), path
        assert translated[path] != said or path.endswith(("vpn.name", "unit_of_measurement")), path


@pytest.mark.parametrize("reason", list(Reason))
def test_every_reason_is_said_on_the_form_and_as_a_failure(reason: Reason) -> None:
    assert f"config.error.{reason}" in ENGLISH
    assert f"exceptions.{reason}.message" in ENGLISH


@pytest.mark.parametrize("standing", STANDINGS)
def test_every_standing_has_its_words(standing: str) -> None:
    assert f"entity.sensor.health.state.{standing}" in ENGLISH


def test_every_entity_has_its_name_and_icon() -> None:
    icons = leaves(load("icons.json"))
    sensors = [one.translation_key for one in (*DASHBOARD_SENSORS, *FINDINGS_SENSORS)]
    assert len(FINDINGS_SENSORS) == len(SEVERITIES)
    for key in sensors:
        assert f"entity.sensor.{key}.name" in ENGLISH
        assert f"entity.sensor.{key}.default" in icons
    for one in DASHBOARD_BINARY_SENSORS:
        assert f"entity.binary_sensor.{one.translation_key}.name" in ENGLISH
