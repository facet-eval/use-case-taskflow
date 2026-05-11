# Contributing to taskflow

Welcome. This document defines how we work on this project. Read it once before opening your first PR.

## Branching model

`main` is the only long-lived branch. All work happens on short-lived feature branches that target `main` via pull request. Branch names follow the pattern `<type>/<slug>` where `<type>` matches the Conventional Commit type (`feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `ci`) and `<slug>` is a short kebab-case description of the change.

Examples: `feat/list-command`, `fix/due-date-tz`, `refactor/repository-layer`.

Branches are deleted as soon as their PR is merged.

## Merge strategy

We squash and merge. Every PR collapses into a single commit on `main`. The intra-branch history can be informal (work-in-progress commits, "fix lint", "address review") because it is discarded at merge time. The squash-merge subject is what survives, so it follows the commit convention strictly (see below).

Why squash: it keeps `main` linear and reviewable. Every commit on `main` is a complete, atomic change that can be read, reverted, or bisected on its own.

## Commit convention

Squash-merge commits use Conventional Commits with a Gitmoji at the front of the subject:

```
<type>(<scope>): <emoji> <subject> (#<pr-number>)
```

Types and emojis used in this project:

| Type     | Emoji | When to use                                        |
|----------|-------|----------------------------------------------------|
| feat     | ✨    | New user-facing capability                         |
| fix      | 🐛    | Bug fix; ship a regression test where feasible     |
| refactor | ♻️    | Internal change, behavior preserved                |
| docs     | 📝    | Documentation-only change                          |
| test     | ✅    | Test-only change                                   |
| chore    | 🔧    | Tooling, deps, config that doesn't ship to users   |
| ci       | 👷    | CI pipeline change                                 |

Inside a feature branch you may use any commit messages that help you. They will not appear on `main`.

## Pull request requirements

Every PR uses the template at `.github/PULL_REQUEST_TEMPLATE.md`. The four sections are required:

- **Context** — what problem this solves and why now.
- **Changes** — what changed, in plain language.
- **Testing** — what you ran and the result.
- **Related issue** — `Closes #N`.

CI must pass before merging. The PR title follows the same Conventional + Gitmoji format as the squash-merge commit.

## Issue conventions

Bugs use `.github/ISSUE_TEMPLATE/bug_report.md`. A good bug report contains:

- Reproducible steps (commands you ran).
- The expected behavior.
- The actual behavior.
- Environment (OS, Python version, install method).

Feature requests use `.github/ISSUE_TEMPLATE/feature_request.md`. A good feature request contains:

- The problem you have, before any proposed solution.
- The proposal.
- Alternatives you considered.
- Acceptance criteria.

## Reviews

Reviews are substantive. **LGTM-only comments are forbidden — silence is preferred over filler.** When you review:

- Request a concrete change when something is wrong.
- Ask a clarifying question when intent is unclear.
- Stay silent when the change is straightforward and correct. The merge action is the approval signal.

Self-approval is blocked by GitHub. That is fine: a merge by the author after a substantive review thread (or after silent agreement) is the canonical approval here.

## Code style

- English everywhere — code, comments, commit messages, PR bodies, issues.
- Comments are reserved for genuinely obscure logic. Prefer self-documenting code via clear naming and structure. The codebase aims for effectively zero comments.
- Formatting and linting: `ruff format` and `ruff check`. Configuration lives in `pyproject.toml`.
- Type checking: `mypy --strict src/`.

## Testing expectations

Tests are required for:

- New user-facing behavior (`feat`).
- Bug fixes (`fix`) — include a regression test that fails on `main` and passes on the branch.
- New repository methods (`refactor` that introduces a new abstraction).

Tests **may be deferred** when:

- The change is a mechanical refactor with full behavior coverage from existing integration tests.
- The change is documentation-only or CI-only.
- The change is so small that adding a test would be ceremony (a typo in a help string, for example).

When tests are deferred, the PR's **Testing** section says so explicitly, and a follow-up issue is opened if focused tests would still be valuable later.
