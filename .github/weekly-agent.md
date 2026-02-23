# Weekly Maintenance Agent

This document explains the automated weekly maintenance workflow for the
`rohandesai007/EMRV` repository.

---

## Overview

The workflow lives at `.github/workflows/weekly-maintenance.yml`.
It runs automatically at **2:00 PM America/Chicago (Central Time) every Monday
and Wednesday**, and can also be triggered manually from the **Actions** tab on
GitHub.

### Schedule and DST handling

GitHub Actions `schedule` uses UTC and does not support time zones directly.
To handle daylight saving time (DST) correctly, the workflow uses **two cron
entries per day** — one for CDT (UTC−5) and one for CST (UTC−6):

| UTC cron | Offset | Local time |
|----------|--------|------------|
| `0 19 * * 1` | CDT (UTC−5) | Mon 14:00 CT |
| `0 20 * * 1` | CST (UTC−6) | Mon 14:00 CT |
| `0 19 * * 3` | CDT (UTC−5) | Wed 14:00 CT |
| `0 20 * * 3` | CST (UTC−6) | Wed 14:00 CT |

Because both entries always fire, a **DST-safe time gate** step runs first in
the job. It checks the current hour and day in `America/Chicago`; if the local
time is not 14:00 on Monday or Wednesday, it sets `should_run=false` and all
subsequent steps are skipped. Only the cron fire that truly lands at 14:00 CT
proceeds. Manual `workflow_dispatch` runs bypass the gate entirely.

When changes are produced **and** tests pass, it opens a pull request from a
branch named `bot/weekly-maintenance-YYYY-MM-DD`.  The PR body includes a
summary of what ran and links to lint/test output for easy review.

---

## What it does

### Phase A – Safe mechanical improvements (enabled by default)

| Step | Tool | Effect |
|------|------|--------|
| Code formatting | `black` | Rewrites Python files to comply with the configured line length |
| Import sorting | `isort` | Reorders imports to the `black`-compatible profile |
| Lint report | `flake8` | Reports code-style findings in the PR body; **never blocks** the PR |

### Phase B – Guardrailed refactors (disabled by default)

Phase B is a placeholder for more aggressive automated refactors (e.g.,
`pyupgrade`, `autoflake`).  Enable it in `.github/weekly-agent.yml` once you
have defined which commands to run.

---

## Guardrails configuration (`.github/weekly-agent.yml`)

All behaviour is controlled through `.github/weekly-agent.yml`:

```yaml
guardrails:
  max_files_changed: 30       # Revert all changes if more files are modified
  max_lines_changed: 400      # Revert all changes if more lines are touched
  include_paths:              # Glob patterns the agent may touch
    - "emrvalidator-github/emrvalidator/**"
    - "emrvalidator-github/tests/**"
  exclude_paths:              # Glob patterns the agent must skip
    - "dist/**"
    - "*.tar.gz"
  never_touch:                # Specific files that must NEVER be modified
    - ".github/workflows/weekly-maintenance.yml"
    - ".github/weekly-agent.yml"
    - "emrvalidator-github/pyproject.toml"

phases:
  phase_a:
    enabled: true
  phase_b:
    enabled: false            # Set to true to enable experimental refactors

open_pr_on_test_failure: false  # Set to true to open PR even when tests fail
```

### Key guardrail options

| Key | Default | Description |
|-----|---------|-------------|
| `max_files_changed` | `30` | Maximum number of files allowed to change per run. All changes are reverted if exceeded. |
| `max_lines_changed` | `400` | Maximum total insertions + deletions per run. All changes are reverted if exceeded. |
| `include_paths` | `emrvalidator-github/**` | Glob patterns of paths the agent may modify. |
| `exclude_paths` | `dist/**, *.tar.gz` | Paths that are always skipped. |
| `never_touch` | *(list)* | Absolute file paths that may never be modified; violations cause an immediate revert. |
| `phases.phase_a.enabled` | `true` | Enable/disable formatting + lint report. |
| `phases.phase_b.enabled` | `false` | Enable/disable experimental refactor step. |
| `open_pr_on_test_failure` | `false` | When `true`, opens a PR even when tests fail (failure is noted in the PR body). |

---

## Running manually

1. Go to **Actions** → **Weekly Maintenance** in the GitHub repository.
2. Click **Run workflow** → **Run workflow**.
3. The job will appear in the queue within a few seconds.

---

## PR behaviour

- Branch name: `bot/weekly-maintenance-YYYY-MM-DD`
- PR title: `Weekly maintenance (YYYY-MM-DD)`
- If the branch already exists from a previous run on the same date,
  `peter-evans/create-pull-request` will update the existing PR.
- **No PR is opened** when:
  - No changes were produced after formatting.
  - Guardrails were breached (changes reverted).
  - Tests failed (unless `open_pr_on_test_failure: true`).

---

## Required permissions

The workflow uses the built-in `GITHUB_TOKEN` with the following permissions:

```yaml
permissions:
  contents: write       # create branches and push commits
  pull-requests: write  # open and update pull requests
```

No additional secrets are required.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| Workflow runs but no PR created | No formatting changes needed, or tests failed | Check the job logs; increase `open_pr_on_test_failure` temporarily |
| PR reverted immediately | Guardrail breach (`max_files_changed` or `max_lines_changed`) | Raise the limits in `.github/weekly-agent.yml` |
| `never_touch` violation | A formatter modified a protected file | Add a formatter `exclude` pattern or adjust `never_touch` |
| Tests fail on the maintenance branch | Pre-existing test failure or formatter introduced a regression | Fix tests on `main` first; the bot will pick up clean state next run |
