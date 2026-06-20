# Plan 007: Design/spike — Build validation + install CLI

> **Executor instructions**: This is a DESIGN/SPIKE plan, not a
> build-everything plan. Your job is to investigate, prototype the API
> surface, and list open questions — not to ship a production CLI. Follow
> the steps, produce the artifacts, and report findings. If anything in the
> "STOP conditions" section occurs, stop and report — do not improvise.
> When done, update the status row for this plan in `plans/README.md` —
> unless a reviewer dispatched you and told you they maintain the index.
>
> **Drift check (run first)**: `git diff --stat ddd7081..HEAD -- main.py src/ pyproject.toml`
> If these files changed since this plan was written, compare the excerpts
> below against the live code before proceeding; on a mismatch, treat it as
> a STOP condition.

## Status

- **Priority**: P3
- **Effort**: M (design/spike — not a full build)
- **Risk**: LOW
- **Depends on**: none (but conflicts with plan 001 — see dependency notes)
- **Category**: direction
- **Planned at**: commit `ddd7081`, 2026-06-20

## Why this matters

The Python scaffold (`uv init`) exists but does nothing useful — `main.py` is a stub, `src/godmode_pi/` is empty. The natural purpose for Python in this repo is a CLI tool that validates configs and installs them. This would turn dead weight into the repo's primary tool, give users a single `godmode-pi install` command instead of manual `cp` steps, and provide a foundation for future automation (regression testing, model-specific deployment).

However, this is a design/spike because it's not clear whether the repo should have Python at all — the alternative is a shell-script-based approach (plans 003 and 004). This plan investigates the tradeoffs and produces a recommendation.

## Current state

The existing Python scaffold:
- `main.py` — stub: `def main(): print("Hello from godmode-pi!")`
- `src/godmode_pi/__init__.py` — version string only
- `pyproject.toml` — project metadata, dev deps (ruff, mypy, pytest), tool config
- `uv.lock` — 44KB lockfile

The validation logic exists (or will exist) in `scripts/validate.sh` (plan 003).
The install logic exists (or will exist) in `scripts/install.sh` (plan 004).

## Commands you will need

| Purpose | Command | Expected on success |
|---------|---------|---------------------|
| Create venv | `uv venv` | exit 0 |
| Install | `uv sync` | exit 0 |
| Typecheck | `uv run mypy src/` | exit 0 |
| Lint | `uv run ruff check src/` | exit 0 |
| Test | `uv run pytest` | exit 0 or "no tests ran" |

## Scope

**In scope** (the only files you should create/modify):
- `main.py` — rewrite as CLI entry point
- `src/godmode_pi/` — add `cli.py`, `validate.py`, `install.py` modules
- `pyproject.toml` — add `[project.scripts]` entry point
- `tests/` — add `test_validate.py` and `test_install.py`
- `scripts/validate.sh` and `scripts/install.sh` — leave as-is (the CLI wraps them)

**Out of scope** (do NOT touch):
- Any config file — the CLI reads them, doesn't modify
- `README.md` — documentation is a follow-up
- `AGENTS.md` — separate concern
- `.github/` — CI is plan 002

## Git workflow

- Branch: `advisor/007-cli-design-spike`
- Commit message: `spike: prototype CLI tool design for validation and install`
- Do NOT push or open a PR unless the operator instructed it

## Steps

### Step 1: Define the CLI API

Design the CLI interface. The proposed API:

```
godmode-pi validate [--files config.yml prefill.json ...]
    Validate config files. Default: validate all known configs.

godmode-pi install [--dry-run] [--uninstall]
    Install configs to ~/.omp/agent/. Mirrors scripts/install.sh flags.

godmode-pi status
    Show which configs are installed and their status.

godmode-pi --version
    Print version.
```

Write the API design to `src/godmode_pi/CLI.md` (a design doc, not user-facing docs).

**Verify**: `test -f src/godmode_pi/CLI.md` exits 0.

### Step 2: Implement the CLI skeleton

Create `src/godmode_pi/cli.py` with:
- `argparse`-based CLI with subcommands: `validate`, `install`, `status`
- `main()` function registered in `pyproject.toml` as `godmode-pi`
- Each subcommand is a function in its own module

Create `src/godmode_pi/validate.py` with a `validate_all()` function that:
- Reads each config file
- Validates structure (same logic as `scripts/validate.sh` but in Python)
- Returns a list of `(filename, status, message)` tuples

Create `src/godmode_pi/install.py` with:
- `install(dry_run=False)` — copies files to `~/.omp/agent/`
- `uninstall(dry_run=False)` — removes files from `~/.omp/agent/`
- `status()` — checks which files are installed

Update `pyproject.toml`:
```toml
[project.scripts]
godmode-pi = "godmode_pi.cli:main"
```

**Verify**: `uv run godmode-pi --help` exits 0 and shows subcommands.

### Step 3: Implement validate subcommand

Port the validation logic from `scripts/validate.sh` into `src/godmode_pi/validate.py`:
- YAML validation (using stdlib or `import yaml` if available)
- JSON validation (stdlib `json`)
- Modelfile directive checks (regex)
- Markdown non-empty checks

**Verify**: `uv run godmode-pi validate` exits 0 and prints OK for all files.

### Step 4: Implement install subcommand

Port the install logic from `scripts/install.sh` into `src/godmode_pi/install.py`:
- Same flags: `--dry-run`, `--uninstall`
- Same safety: backup existing `config.yml`, never overwrite without backup
- Same idempotency: running install twice is safe

**Verify**: `uv run godmode-pi install --dry-run` prints planned actions without modifying files.

### Step 5: Write tests

Create `tests/test_validate.py`:
- Test that valid configs pass
- Test that malformed YAML/JSON fails
- Test that missing files fail gracefully

Create `tests/test_install.py`:
- Test dry-run mode (no files modified)
- Test install to a temp directory (use `--prefix` or mock `~/.omp/agent/`)

**Verify**: `uv run pytest tests/ -v` exits 0, tests pass.

### Step 6: Report findings

Write a brief report to `plans/007-cli-report.md` covering:
1. Whether the Python CLI approach is worth pursuing over shell scripts
2. Key tradeoffs: dependency burden (PyYAML?) vs. shell portability
3. Open questions: should `scripts/validate.sh` and `scripts/install.sh` be deprecated?
4. Effort estimate to ship a production-ready CLI

**Verify**: `test -f plans/007-cli-report.md` exits 0.

## Test plan

Tests in `tests/`:
- `test_validate.py` — 3-5 test cases (valid configs, bad YAML, bad JSON, missing file, wrong structure)
- `test_install.py` — 2-3 test cases (dry-run prints actions, install to temp dir, uninstall from temp dir)

Pattern: use `pytest` and `tmp_path` fixture for file operations.

## Done criteria

ALL must hold:

- [ ] `src/godmode_pi/CLI.md` exists with the API design
- [ ] `uv run godmode-pi --help` exits 0 and shows validate/install/status subcommands
- [ ] `uv run godmode-pi validate` exits 0
- [ ] `uv run godmode-pi install --dry-run` exits 0
- [ ] `uv run pytest tests/ -v` exits 0 with at least 5 tests
- [ ] `plans/007-cli-report.md` exists with findings
- [ ] `git status --short` is clean
- [ ] `plans/README.md` status row updated

## STOP conditions

Stop and report back (do not improvise) if:

- `main.py` or `src/godmode_pi/` have been deleted (plan 001 was executed first — in that case, this plan needs to re-create the Python scaffold, which changes the scope).
- `pyproject.toml` has been deleted (same conflict with plan 001).
- The `yaml` module is not available and `pip install pyyaml` fails — document this as an open question in the report.
- Any config file has a different structure than described in plan 003's "Current state."

## Maintenance notes

- This plan conflicts with plan 001 (remove Python scaffold). If plan 001 is executed first, this plan must re-create the Python project structure. If this plan is executed first, plan 001 should be skipped or revised.
- The shell scripts (`scripts/validate.sh`, `scripts/install.sh`) serve as the reference implementation. The Python CLI should produce identical behavior.
- Consider using `click` or `typer` instead of `argparse` for a better DX — note this in the report.
