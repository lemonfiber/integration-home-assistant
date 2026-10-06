# Task runner for lemonfiber/integration-home-assistant. `uv run just` with no argument lists the tasks.
#
# `just` is a dev dependency, so `uv run just <task>` works in any clone after
# `uv sync`. Every task runs its tools through `uv run`, so the versions are the
# ones `uv.lock` pins.
default:
    @just --list

# Turn on the repository's own git hooks. Once per clone; `ci` does it too.
hooks:
    git config core.hooksPath .githooks
    @echo "hooks on: .githooks/pre-commit, .githooks/commit-msg, .githooks/pre-push"

# Everything the `checks` and `tests and coverage` jobs run. Mutation, hassfest,
# HACS, the vendored client's drift and the shared workflows are CI's alone.
ci: hooks lint types coverage

# Formatting and every lint rule, changing nothing.
lint:
    uv run ruff format --check .
    uv run ruff check .

# Format, apply the fixes ruff can make, and format what they changed.
fix:
    uv run ruff format .
    uv run ruff check --fix .
    uv run ruff format .

# Pyright in strict mode over the integration, the tests and the scripts.
types:
    uv run pyright

# The suite alone.
test *args:
    uv run pytest {{args}}

# The suite with 100% line and branch coverage required, and the report the
# SonarQube Cloud scan reads written to `coverage.xml`.
coverage:
    uv run pytest --cov --cov-report=term-missing --cov-report=xml

# Replace the vendored client with sdk-python at a full commit hash.
vendor commit:
    uv run python scripts/vendor_sdk.py take {{commit}}

# The vendored client against the commit it records, and against sdk-python's main.
vendor-check:
    uv run python scripts/vendor_sdk.py check

# Mutation testing and the minimum score. Slow: CI runs it on every pull request.
mutation:
    uv run mutmut run
    uv run mutmut export-cicd-stats
    uv run python scripts/mutation_score.py
