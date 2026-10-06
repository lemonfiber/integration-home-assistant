# Copyright (c) 2026 NightWorksIO
"""The rules the tree is built to: the stack is reached through sdk-python alone, with a key and never a password."""

import ast
import pathlib
import re
from typing import Final

import pytest

ROOT: Final = pathlib.Path(__file__).resolve().parent.parent
INTEGRATION: Final = ROOT / "custom_components" / "lemonfiber"
VENDOR: Final = INTEGRATION / "_vendor"
SHARED_GATE: Final = ROOT / "scripts" / "no_open_codeql_alert.py"

SUPPRESSIONS: Final = re.compile(
    r"#\s*(type:\s*ignore|pyright:|noqa|pragma:\s*no\s*(cover|branch))",
    re.IGNORECASE,
)
WIRE: Final = frozenset({"aiohttp", "urllib3", "requests", "httpx", "http", "socket", "ssl", "urllib"})
"""Every way to reach a stack that is not sdk-python."""


def python_files(*roots: pathlib.Path) -> list[pathlib.Path]:
    """Return every Python file under these roots but the vendored client and the shared gate's copy."""
    return sorted(
        path
        for root in roots
        for path in root.rglob("*.py")
        if path != SHARED_GATE and VENDOR not in path.parents
    )


def imported(path: pathlib.Path) -> set[str]:
    """Return the top-level name of every module a file imports."""
    names: set[str] = set()
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Import):
            names.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None and node.level == 0:
            names.add(node.module.split(".")[0])
    return names


@pytest.mark.parametrize("path", python_files(INTEGRATION, ROOT / "tests", ROOT / "scripts"), ids=str)
def test_nothing_silences_a_checker(path: pathlib.Path) -> None:
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        assert not SUPPRESSIONS.search(line), f"{path}:{number} silences a checker"


@pytest.mark.parametrize("path", python_files(INTEGRATION), ids=str)
def test_the_stack_is_reached_through_sdk_python_alone(path: pathlib.Path) -> None:
    assert not imported(path) & WIRE, f"{path} reaches past sdk-python"


@pytest.mark.parametrize("path", python_files(INTEGRATION), ids=str)
def test_no_password_is_asked_for_or_exchanged(path: pathlib.Path) -> None:
    source = path.read_text(encoding="utf-8")
    assert "admit" not in {node.id for node in ast.walk(ast.parse(source)) if isinstance(node, ast.Name)}
    assert "admit_async" not in source
    assert "CONF_PASSWORD" not in source


@pytest.mark.parametrize("path", python_files(INTEGRATION), ids=str)
def test_no_module_declares_a_response_shape(path: pathlib.Path) -> None:
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.ClassDef):
            assert not {ast.unparse(base) for base in node.bases} & {"TypedDict", "typing.TypedDict"}, path
