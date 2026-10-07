# Copyright (c) 2026 NightWorksIO
"""The answer `what changed` gives, which decides whether the code gates run."""

from typing import TYPE_CHECKING

import pytest

from scripts import the_code_a_change_touches as touches

if TYPE_CHECKING:
    import pathlib
    from collections.abc import Mapping

PIN = "      uses: lemonfiber/spec/.github/workflows/dco.yml@{} # v1.0.{}\n"
WORKFLOW = "jobs:\n  dco:\n" + PIN.format("a" * 40, 1) + "  checks:\n    runs-on: ubuntu-latest\n"
MOVED = WORKFLOW.replace(PIN.format("a" * 40, 1), PIN.format("b" * 40, 2))
CHANGED = WORKFLOW.replace("ubuntu-latest", "ubuntu-24.04")
GATED = (".github/workflows/ci.yml", ".github/workflows/sonar.yml", ".github/workflows/validate.yml")
TREE = {
    "README.md": "a",
    "docs/guide.md": "a",
    "LICENSE": "a",
    "custom_components/lemonfiber/sensor.py": "a",
    ".github/workflows/ci.yml": WORKFLOW,
    ".github/workflows/sonar.yml": WORKFLOW,
    ".github/workflows/validate.yml": WORKFLOW,
    ".github/workflows/codeql.yml": "a",
    ".github/dependabot.yml": "a",
}


def git(root: pathlib.Path, *args: str) -> str:
    who = ("-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false")
    return touches.git(root, *who, *args).stdout.strip()


def commit(root: pathlib.Path, files: Mapping[str, str | None]) -> str:
    for name, text in files.items():
        path = root / name
        if text is None:
            path.unlink()
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
    git(root, "add", "-A")
    git(root, "commit", "-q", "--allow-empty", "-m", "x")
    return git(root, "rev-parse", "HEAD")


@pytest.fixture
def base(tmp_path: pathlib.Path) -> str:
    git(tmp_path, "init", "-q")
    return commit(tmp_path, TREE)


@pytest.mark.parametrize(
    ("files", "code", "hacs", "analyze"),
    [
        ({}, False, False, False),
        ({"docs/guide.md": "b", "LICENSE": "b", "AGENTS.md": "b"}, False, False, False),
        ({"README.md": "b"}, False, True, False),
        ({"docs/guide.md": None}, False, False, False),
        ({"custom_components/lemonfiber/README.md": "b"}, False, False, False),
        ({"docs/guide.md": "b", "custom_components/lemonfiber/sensor.py": "b"}, True, True, True),
        ({"custom_components/lemonfiber/sensor.py": None, "docs/sensor.md": "a"}, True, True, True),
        ({"hacs.json": "b"}, True, True, True),
        ({"notes.txt": "b"}, True, True, True),
        (dict.fromkeys(GATED, MOVED), False, False, True),
        ({".github/workflows/ci.yml": CHANGED}, True, True, True),
        ({".github/workflows/sonar.yml": CHANGED}, True, True, True),
        ({".github/workflows/validate.yml": CHANGED}, True, True, True),
        ({".github/workflows/validate.yml": None}, True, True, True),
        ({".github/workflows/codeql.yml": "b", ".github/dependabot.yml": "b"}, False, False, True),
        ({"scripts/the_code_a_change_touches.py": "b"}, True, True, True),
    ],
    ids=[
        "nothing at all",
        "a guide, the license and the agent guide",
        "the readme HACS renders",
        "a guide deleted",
        "Markdown under the integration",
        "a module beside a guide",
        "a module moved into the docs",
        "the HACS manifest",
        "a file of a kind nobody listed",
        "pins moved in the gated workflows",
        "a job changed in ci.yml",
        "a job changed in sonar.yml",
        "a job changed in validate.yml",
        "validate.yml deleted",
        "workflows that run no gate this decides",
        "this script",
    ],
)
def test_each_change_reaches_the_gates_that_read_it(
    tmp_path: pathlib.Path,
    base: str,
    files: dict[str, str | None],
    *,
    code: bool,
    hacs: bool,
    analyze: bool,
) -> None:
    commit(tmp_path, files)
    answer, why = touches.decide(tmp_path, base)
    assert answer == {"code": code, "hacs": hacs, "analyze": analyze}, why


@pytest.mark.parametrize("missing", ["", "0" * 40, "f" * 40, "HEAD", "--output=x"])
def test_a_base_that_is_no_commit_runs_every_gate(tmp_path: pathlib.Path, base: str, missing: str) -> None:
    assert base
    answer, why = touches.decide(tmp_path, missing)
    assert answer == {"code": True, "hacs": True, "analyze": True}
    assert why == [f"No commit `{missing}` to compare against, so every gate runs."]


def test_the_answer_is_written_where_the_workflow_and_a_person_read_it(
    tmp_path: pathlib.Path,
    base: str,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    commit(tmp_path, {"docs/guide.md": "b", ".github/dependabot.yml": "b"})
    output, summary = tmp_path / "output", tmp_path / "summary"
    monkeypatch.setenv("GITHUB_OUTPUT", str(output))
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(summary))
    assert touches.run([base], tmp_path) == 0
    assert output.read_text(encoding="utf-8") == "code=false\nhacs=false\nanalyze=true\n"
    assert "- `.github/dependabot.yml: analyze`\n" in summary.read_text(encoding="utf-8")
    assert (
        capsys.readouterr().out
        == "code=false\nhacs=false\nanalyze=true\n.github/dependabot.yml: analyze\ndocs/guide.md: no gate\n"
    )


def test_outside_a_workflow_the_answer_is_only_said(
    tmp_path: pathlib.Path,
    base: str,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.delenv("GITHUB_OUTPUT", raising=False)
    monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)
    assert touches.run([base], tmp_path) == 0
    assert capsys.readouterr().out == "code=false\nhacs=false\nanalyze=false\n"


@pytest.mark.parametrize("argv", [[], ["a", "b"]])
def test_anything_but_one_base_is_refused(tmp_path: pathlib.Path, argv: list[str]) -> None:
    assert touches.run(argv, tmp_path) == 2
