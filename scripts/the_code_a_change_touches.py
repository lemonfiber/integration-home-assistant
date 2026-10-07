# Copyright (c) 2026 NightWorksIO
"""Decide whether a change touches code, so the jobs that judge only code can skip one that does not.

A pull request that changes only documentation holds runners for the Python
toolchain, the test suite, mutation testing, the coverage run, the SonarCloud
scan, Home Assistant's and HACS's validation and the CodeQL analysis, and none
of them can answer differently than it did on the base. So each of those jobs
asks this first, through a `what changed` job, and skips where the answer is
no. `ci.yml`, `sonar.yml`, `validate.yml` and `codeql.yml` each run that job,
and all four run this script, so they cannot disagree about a path.

It answers once per kind of gate, as a line written to `$GITHUB_OUTPUT`:

  code     the Python gates in `ci.yml`, the coverage run and scan in
           `sonar.yml` and `hassfest` in `validate.yml`. Documentation is not
           code: `docs/`, any Markdown file and `LICENSE`, none of which those
           gates read. Nor is anything under `.github/` but the three
           workflows that run them, and those three neither where every line a
           change makes to them is a pin on a shared workflow from
           `lemonfiber/spec`, since a shared workflow runs none of those gates.
  hacs     the HACS check in `validate.yml`, which reads what `code` reads and
           `README.md` as well: `hacs.json` has HACS render it.
  analyze  the CodeQL analyses, one of which reads `.github/`. Only
           documentation is not code for them.

Anything not named as documentation is code, so a file of a kind nobody has
thought about runs every gate. A rename is read as the deletion and the addition
it is, so moving a module into `docs/` reaches code through the deletion.

Asked about nothing it can compare (no base, a base that is not a commit here,
a push that opened a branch) it answers yes for every gate. So does a run that
fails: the jobs asking run whenever the `what changed` job did not succeed.

    python3 scripts/the_code_a_change_touches.py <base>
"""

import os
import pathlib
import re
import subprocess
import sys

GATES: tuple[str, ...] = ("code", "hacs", "analyze")
"""The gates this answers for, in the order their lines are written."""

GATED = frozenset(
    {".github/workflows/ci.yml", ".github/workflows/sonar.yml", ".github/workflows/validate.yml"},
)
"""The workflows that run the gates `code` decides."""

PIN = re.compile(r"[-+]\s*uses: lemonfiber/spec/\.github/workflows/[^@]+@[0-9a-f]{40}( # .*)?")
"""A changed line that moves a pin on a shared workflow and nothing else."""

RENDERED = "README.md"
"""The documentation HACS reads, since `hacs.json` has it render the readme."""


def git(root: pathlib.Path, *args: str) -> subprocess.CompletedProcess[str]:
    """Run git in `root`, failing on anything but success."""
    return subprocess.run(["git", *args], cwd=root, capture_output=True, check=True, text=True)


def documentation(path: str) -> bool:
    """Return whether this path is documentation, which no gate reads but for the readme HACS renders."""
    return path.startswith("docs/") or path.endswith(".md") or path == "LICENSE"


def only_pins(root: pathlib.Path, base: str, path: str) -> bool:
    """Return whether every line the change makes to `path` is a pin on a shared workflow."""
    diff = git(root, "diff", "-U0", base, "HEAD", "--", path).stdout
    changed = [
        line for line in diff.splitlines() if line[:1] in "+-" and not line.startswith(("+++ ", "--- "))
    ]
    return all(PIN.fullmatch(line) for line in changed)


def reaches(root: pathlib.Path, base: str, path: str) -> dict[str, bool]:
    """Return which gates one changed path reaches."""
    if documentation(path):
        return {"code": False, "hacs": path == RENDERED, "analyze": False}
    code = not only_pins(root, base, path) if path in GATED else not path.startswith(".github/")
    return {"code": code, "hacs": code, "analyze": True}


def changed(root: pathlib.Path, base: str) -> list[str] | None:
    """Return each path HEAD changes against `base`, or None where `base` is not a commit."""
    if not base:
        return None
    try:
        git(root, "cat-file", "-e", f"{base}^{{commit}}")
    except subprocess.CalledProcessError:
        return None
    return git(root, "diff", "--no-renames", "--name-only", "-z", base, "HEAD").stdout.split("\0")[:-1]


def decide(root: pathlib.Path, base: str) -> tuple[dict[str, bool], list[str]]:
    """Return which gates the change reaches, and the lines that say why."""
    paths = changed(root, base)
    if paths is None:
        return dict.fromkeys(GATES, True), [f"No commit `{base}` to compare against, so every gate runs."]
    answer = dict.fromkeys(GATES, False)
    why: list[str] = []
    for path in paths:
        gates = [gate for gate, hit in reaches(root, base, path).items() if hit]
        answer.update(dict.fromkeys(gates, True))
        why.append(f"{path}: {', '.join(gates) or 'no gate'}")
    return answer, why


def report(answer: dict[str, bool], why: list[str]) -> None:
    """Write the answer where the workflow reads it, and the reason where a person does."""
    lines = [f"{gate}={str(answer[gate]).lower()}" for gate in GATES]
    sys.stdout.write("".join(f"{line}\n" for line in [*lines, *why]))
    if output := os.environ.get("GITHUB_OUTPUT"):
        with pathlib.Path(output).open("a", encoding="utf-8") as out:
            out.write("".join(f"{line}\n" for line in lines))
    if summary := os.environ.get("GITHUB_STEP_SUMMARY"):
        with pathlib.Path(summary).open("a", encoding="utf-8") as out:
            out.write("### What changed\n\n" + "".join(f"- `{line}`\n" for line in [*lines, *why]))


def run(argv: list[str], root: pathlib.Path) -> int:
    """Decide for HEAD against the one base given."""
    if len(argv) != 1:
        sys.stderr.write("usage: the_code_a_change_touches.py <base>\n")
        return 2
    report(*decide(root, argv[0]))
    return 0


if __name__ == "__main__":
    sys.exit(run(sys.argv[1:], pathlib.Path.cwd()))
