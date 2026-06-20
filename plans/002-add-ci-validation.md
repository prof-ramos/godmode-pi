# Plan 002: Add GitHub Actions CI for config validation

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md` — unless a reviewer dispatched you and told you they
> maintain the index.
>
> **Drift check (run first)**: `git diff --stat ddd7081..HEAD -- .github/`
> If `.github/` already exists and has content, compare against the plan's
> assumptions before proceeding; on a mismatch, treat it as a STOP condition.

## Status

- **Priority**: P1
- **Effort**: S
- **Risk**: LOW
- **Depends on**: none (but benefits from plan 003 existing — the CI can run the validation script)
- **Category**: dx
- **Planned at**: commit `ddd7081`, 2026-06-20

## Why this matters

This repo distributes configuration files (`config.yml`, `prefill.json`, `Modelfile-godmode`, `APPEND_SYSTEM.md`, `RULES.md`) that directly affect agent behavior. A malformed YAML, JSON, or Modelfile pushed to `main` has zero automated guard. CI is the primary quality mechanism for a config-only repo — it catches syntax errors, structural issues, and drift before they reach consumers.

## Current state

No `.github/` directory exists. No CI configuration of any kind. The only verification path is manual (`omp -p`).

The config files that should be validated:
- `config.yml` — YAML with a `systemPrompt` array of strings
- `prefill.json` — JSON array of `{role, content}` message objects
- `Modelfile-godmode` — Ollama Modelfile with `FROM`, `PARAMETER`, `SYSTEM` directives
- `APPEND_SYSTEM.md` — Markdown with numbered rules
- `RULES.md` — Markdown with bulleted rules

## Commands you will need

| Purpose | Command | Expected on success |
|---------|---------|---------------------|
| Check YAML | `python3 -c "import yaml; yaml.safe_load(open('config.yml'))"` | exit 0 |
| Check JSON | `python3 -c "import json; json.load(open('prefill.json'))"` | exit 0 |
| Check Modelfile | `head -1 Modelfile-godmode \| grep -q '^FROM'` | exit 0 |
| Lint Markdown | `grep -c '^#' APPEND_SYSTEM.md` | > 0 |

## Scope

**In scope** (the only files you should create/modify):
- `.github/workflows/validate.yml` — create

**Out of scope** (do NOT touch):
- Any config file — validation is CI-only, no config changes
- `README.md` — badge can be added in a follow-up
- Any Python tooling — use shell commands and stdlib Python for validation

## Git workflow

- Branch: `advisor/002-add-ci-validation`
- Commit message: `ci: add GitHub Actions workflow for config validation`
- Do NOT push or open a PR unless the operator instructed it

## Steps

### Step 1: Create the workflow directory

```bash
mkdir -p .github/workflows
```

**Verify**: `test -d .github/workflows` exits 0.

### Step 2: Create `.github/workflows/validate.yml`

Create a GitHub Actions workflow with:

- **Trigger**: on `push` to `main` and on `pull_request` to `main`
- **Jobs**: one job `validate` running on `ubuntu-latest`
- **Steps**:
  1. Checkout the repo
  2. Validate `config.yml` is valid YAML: `python3 -c "import yaml; yaml.safe_load(open('config.yml')); print('config.yml: OK')"`
  3. Validate `prefill.json` is valid JSON: `python3 -c "import json; d=json.load(open('prefill.json')); assert isinstance(d, list); assert all('role' in m and 'content' in m for m in d); print('prefill.json: OK')"`
  4. Validate `Modelfile-godmode` has required directives: `head -1 Modelfile-godmode | grep -q '^FROM'` and `grep -q '^SYSTEM' Modelfile-godmode`
  5. Validate `APPEND_SYSTEM.md` has content: `test -s APPEND_SYSTEM.md`
  6. Validate `RULES.md` has content: `test -s RULES.md`
  7. Validate `README.md` has no broken internal links: `grep -oP '\[.*?\]\(.*?\)' README.md | grep -v '^http' | sed 's/.*(//;s/)//' | while read f; do test -f "$f" || test -d "$f" || echo "MISSING: $f"; done`

Each step should use `run:` with the shell command. Use `set -e` so any failure stops the job.

**Verify**: The file exists and is valid YAML:
```bash
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/validate.yml')); print('workflow: OK')"
```

### Step 3: Commit

```bash
git add .github/ && git commit -m "ci: add GitHub Actions workflow for config validation"
```

**Verify**: `git log --oneline -1` shows the commit message.

## Test plan

No runtime tests — this is CI configuration. Verification is:
1. The workflow file parses as valid YAML (step 2 verify)
2. Each validation command works when run locally (run them manually)

## Done criteria

ALL must hold:

- [ ] `.github/workflows/validate.yml` exists and is valid YAML
- [ ] `python3 -c "import yaml; yaml.safe_load(open('config.yml'))"` exits 0
- [ ] `python3 -c "import json; json.load(open('prefill.json'))"` exits 0
- [ ] `head -1 Modelfile-godmode | grep -q '^FROM'` exits 0
- [ ] `grep -q '^SYSTEM' Modelfile-godmode` exits 0
- [ ] `test -s APPEND_SYSTEM.md` exits 0
- [ ] `test -s RULES.md` exits 0
- [ ] `git status --short` is clean
- [ ] `plans/README.md` status row updated

## STOP conditions

Stop and report back (do not improvise) if:

- `.github/` already exists with content that would conflict.
- Any config file has been removed or renamed since this plan was written.
- The repo is not hosted on GitHub (check `git remote -v`).

## Maintenance notes

- When new config files are added to the repo, add corresponding validation steps to this workflow.
- The validation uses stdlib Python only — no external dependencies. If the repo later adds Python tooling, consider switching to `uv run` for validation.
- Consider adding a status badge to `README.md` once the workflow runs: `![CI](https://github.com/prof-ramos/godmode-pi/actions/workflows/validate.yml/badge.svg)`
