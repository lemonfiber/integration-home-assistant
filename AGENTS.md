# AGENTS.md — integration-home-assistant

> **Start at the roadmap and board on [lemonfiber.app](https://lemonfiber.app),
> rendered from the report of where every unreleased version stands. Then the
> rules** every repository shares:
> [working in the repositories](https://github.com/lemonfiber/spec/blob/main/50-governance/working-in-the-repositories.md)
> and [the rules for agents](https://github.com/lemonfiber/spec/blob/main/50-governance/ai-contributors.md).
> This file holds only what is true of this repository.

## What this repo is

lemonfiber in Home Assistant: a custom integration with the domain `lemonfiber`,
installed through HACS from this repository. Spec:
[`30-repos/integration-home-assistant.md`](https://github.com/lemonfiber/spec/blob/main/30-repos/integration-home-assistant.md)
and [F12](https://github.com/lemonfiber/spec/blob/main/10-functional/features/f-extensibility/f12-home-assistant.md).

## The rules you cannot break

- **The stack is reached through sdk-python alone, with an integration key.**
  No module imports an HTTP library, and nothing asks for, accepts or stores the
  operator password (`F12-R1`); the architecture tests refuse both.
- **`custom_components/lemonfiber/_vendor/` is not edited by hand.** It is
  sdk-python at the commit its `REVISION` names, written by
  `uv run just vendor <commit>`. `sdk-drift` fails on any difference from that
  commit, and when sdk-python's `main` has changed what the copy holds.
  `sdk-bump` takes that `main` on its own pull request whenever sdk-python's
  `main` moves, and merges it when lint, types and the suite still pass.
- **What appears is what the key's scope reaches**, read from the stack's
  capabilities on every connection, never inferred or asked of the person.
- **No suppressions.** No `# type: ignore`, `# pyright:`, `# noqa` or
  `# pragma: no cover`; the architecture tests refuse each of them.
- **Every string shown is translated**, in `strings.json`, `translations/en.json`
  (identical to it) and `translations/nl.json` (`F12-R11`).

## Checks

```
uv run just ci        # lint, strict types, coverage
uv run just fix       # format and apply the fixes ruff can make
uv run just test      # the suite alone
```

Mutation testing (`just mutation`), `hassfest`, HACS's validation and
`sdk-drift` are merge gates that run in CI.

## Before you open a PR

- `uv run just ci` is clean.
- `custom_components/lemonfiber/quality_scale.yaml` says where each rule stands.
