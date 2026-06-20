# Plan 001: Remove unused Python scaffold

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md` — unless a reviewer dispatched you and told you they
> maintain the index.
>
> **Drift check (run first)**: `git diff --stat ddd7081..HEAD -- main.py src/ pyproject.toml uv.lock .gitignore`
> If any in-scope file changed since this plan was written, compare the
> "Current state" excerpts against the live code before proceeding; on a
> mismatch, treat it as a STOP condition.

## Status

- **Priority**: P1
- **Effort**: S
- **Risk**: LOW
- **Depends on**: none
- **Category**: tech-debt
- **Planned at**: commit `ddd7081`, 2026-06-20

## Why this matters

The repo is a configuration distribution for OMP jailbreak — it ships YAML, JSON, Markdown, and Modelfile configs. The Python scaffold (`uv init`) was added as infrastructure but has no purpose here: `main.py` is a stub that prints "Hello from godmode-pi!", `src/godmode_pi/` contains only a version string, and `uv.lock` is 44KB of lockfile for zero runtime dependencies. Every `uv sync` is wasted time, and the Python project structure misleads contributors into thinking this is a Python project.

## Current state

The files to remove:

- `main.py` — stub entry point:
  ```python
  def main():
      print("Hello from godmode-pi!")
  if __name__ == "__main__":
      main()
  ```
- `src/godmode_pi/__init__.py` — empty package:
  ```python
  """GODMODE — Persistent jailbreak configuration for Oh My Pi (OMP)."""
  __version__ = "0.1.0"
  ```
- `pyproject.toml` — Python project metadata with dev deps (ruff, mypy, pytest) and tool config
- `uv.lock` — 44KB lockfile
- `.venv/` — virtual environment (gitignored, delete locally)

The `.gitignore` currently has Python-specific entries:
```
# Python
.venv/
__pycache__/
*.pyc
.mypy_cache/
.ruff_cache/
```

## Commands you will need

| Purpose | Command | Expected on success |
|---------|---------|---------------------|
| Check files | `git ls-files main.py src/ pyproject.toml uv.lock` | lists the files |
| Verify removal | `git diff --stat` | shows deletions only |
| Status check | `git status --short` | clean |

## Scope

**In scope** (the only files you should modify):
- `main.py` — delete
- `src/godmode_pi/__init__.py` — delete
- `src/godmode_pi/` — delete the directory
- `pyproject.toml` — delete
- `uv.lock` — delete
- `.gitignore` — remove Python-specific entries (lines 32-37)
- `.venv/` — delete locally (already gitignored)

**Out of scope** (do NOT touch, even though they look related):
- Any config file (`APPEND_SYSTEM.md`, `RULES.md`, `config.yml`, `prefill.json`, `Modelfile-godmode`)
- `README.md` — the README doesn't reference the Python scaffold
- `.opencode/` — unrelated
- `.github/` — doesn't exist yet

## Git workflow

- Branch: `advisor/001-remove-python-scaffold`
- Commit message style: `chore: remove unused Python scaffold`
- One commit for all changes
- Do NOT push or open a PR unless the operator instructed it

## Steps

### Step 1: Delete the files

Delete these files and directory:
- `main.py`
- `src/godmode_pi/__init__.py`
- `src/godmode_pi/` (the directory)
- `pyproject.toml`
- `uv.lock`

**Verify**: `git ls-files --deleted` shows all 5 paths listed.

### Step 2: Remove Python entries from .gitignore

Edit `.gitignore` to remove lines 32-37 (the `# Python` section):
```
# Python
.venv/
__pycache__/
*.pyc
.mypy_cache/
.ruff_cache/
```

Keep everything else intact. The resulting `.gitignore` should end at the `# OpenCode project state` section.

**Verify**: `grep -c "Python\|.venv\|__pycache__\|.mypy_cache\|.ruff_cache" .gitignore` returns 0.

### Step 3: Delete local .venv

```bash
rm -rf .venv/
```

**Verify**: `test ! -d .venv && echo "removed"` prints "removed".

### Step 4: Commit

```bash
git add -A && git commit -m "chore: remove unused Python scaffold"
```

**Verify**: `git log --oneline -1` shows the commit message.

## Test plan

No tests to write — this is a deletion-only plan. Verification is by file inspection.

## Done criteria

ALL must hold:

- [ ] `git ls-files main.py src/ pyproject.toml uv.lock` returns nothing (files deleted from tracking)
- [ ] `test ! -f main.py && test ! -f pyproject.toml && test ! -f uv.lock && test ! -d src/` exits 0
- [ ] `grep -q "Python\|.venv\|__pycache__\|.mypy_cache\|.ruff_cache" .gitignore` exits 1 (no matches)
- [ ] `test ! -d .venv` exits 0
- [ ] `git status --short` is clean
- [ ] `plans/README.md` status row updated

## STOP conditions

Stop and report back (do not improvise) if:

- Any file in the in-scope list has content that differs from the excerpts above (the codebase has drifted).
- A file outside the in-scope list would need modification to make the plan work.
- `pyproject.toml` contains project dependencies beyond the dev deps listed (e.g., someone added runtime deps since this plan was written).

## Maintenance notes

- If a future plan wants to add Python tooling (e.g., a CLI), it will need to re-create `pyproject.toml` and the package structure. That's fine — the point is to not carry dead weight until there's a real use.
- The `.gitignore` Python entries can be re-added if Python tooling returns.
