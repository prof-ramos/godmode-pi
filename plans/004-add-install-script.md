# Plan 004: Add install/deploy script

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md` — unless a reviewer dispatched you and told you they
> maintain the index.
>
> **Drift check (run first)**: `git diff --stat ddd7081..HEAD -- scripts/`
> If `scripts/` already exists, compare its contents against the plan's
> assumptions before proceeding; on a mismatch, treat it as a STOP condition.

## Status

- **Priority**: P2
- **Effort**: S
- **Risk**: LOW
- **Depends on**: none
- **Category**: dx
- **Planned at**: commit `ddd7081`, 2026-06-20

## Why this matters

The README documents 4 manual steps to install the jailbreak config: copy `APPEND_SYSTEM.md`, copy `RULES.md`, optionally create the Ollama model, and verify. Manual `cp` commands are error-prone (wrong destination, missing backup, forgotten steps). An install script makes setup idempotent, testable, and one-command — and serves as the source of truth for what "installed" means.

## Current state

The README (`README.md:77-88`) documents the install process:
```bash
# 1. Copiar os arquivos de configuração
cp APPEND_SYSTEM.md ~/.omp/agent/APPEND_SYSTEM.md
cp RULES.md ~/.omp/agent/RULES.md

# 2. (Opcional) Criar modelo Ollama customizado
ollama create deepseek-godmode -f Modelfile-godmode

# 3. Verificar
omp -p '/extensions'
```

The undo section (`README.md:107-118`) documents removal:
```bash
rm ~/.omp/agent/APPEND_SYSTEM.md
rm ~/.omp/agent/RULES.md
ollama rm deepseek-godmode
```

The config files to deploy:
- `APPEND_SYSTEM.md` → `~/.omp/agent/APPEND_SYSTEM.md`
- `RULES.md` → `~/.omp/agent/RULES.md`
- `config.yml` → `~/.omp/agent/config.yml` (optional — user may already have one)
- `Modelfile-godmode` → used by `ollama create` (not copied directly)
- `prefill.json` → `~/.hermes/profiles/godmode-deepseek/prefill.json` (Hermes Agent)

## Commands you will need

| Purpose | Command | Expected on success |
|---------|---------|---------------------|
| Run install | `bash scripts/install.sh` | exit 0 |
| Run install dry-run | `bash scripts/install.sh --dry-run` | exit 0, no files copied |
| Run uninstall | `bash scripts/install.sh --uninstall` | exit 0 |

## Scope

**In scope** (the only files you should create/modify):
- `scripts/install.sh` — create
- `scripts/` — create directory (if not already created by another plan)

**Out of scope** (do NOT touch):
- `README.md` — the README can be updated to reference the script in a follow-up
- Any config file — the script reads them, doesn't modify
- `~/.omp/agent/` — the script targets this directory but doesn't create it in the repo
- `~/.hermes/` — same

## Git workflow

- Branch: `advisor/004-add-install-script`
- Commit message: `feat: add install/deploy script`
- Do NOT push or open a PR unless the operator instructed it

## Steps

### Step 1: Create the scripts directory (if needed)

```bash
mkdir -p scripts
```

**Verify**: `test -d scripts` exits 0.

### Step 2: Create `scripts/install.sh`

Create a shell script with these capabilities:

**Flags**:
- `--dry-run` — print what would be done without actually copying
- `--uninstall` — remove installed files (reverse of install)
- `--help` — print usage
- No flags — perform install

**Install behavior**:
1. Create `~/.omp/agent/` if it doesn't exist (dry-run: print "mkdir -p ~/.omp/agent/")
2. Copy `APPEND_SYSTEM.md` to `~/.omp/agent/APPEND_SYSTEM.md` (dry-run: print the cp command)
3. Copy `RULES.md` to `~/.omp/agent/RULES.md` (dry-run: print)
4. If `config.yml` exists in repo, copy to `~/.omp/agent/config.yml` with a backup of any existing file (dry-run: print)
5. Print summary of what was installed
6. Exit 0

**Uninstall behavior**:
1. Remove `~/.omp/agent/APPEND_SYSTEM.md` if it exists (dry-run: print)
2. Remove `~/.omp/agent/RULES.md` if it exists (dry-run: print)
3. Print summary of what was removed
4. Exit 0

**Safety**:
- Use `set -euo pipefail` at the top
- Never overwrite without backup (for `config.yml` — the other files are owned by this repo)
- Print clear error messages if source files don't exist
- The `--uninstall` flag should NOT require `ollama rm` — that's destructive and should remain manual

**Verify**: `bash scripts/install.sh --help` prints usage. `bash scripts/install.sh --dry-run` prints what it would do without touching anything.

### Step 3: Make the script executable

```bash
chmod +x scripts/install.sh
```

**Verify**: `test -x scripts/install.sh` exits 0.

### Step 4: Commit

```bash
git add scripts/install.sh && git commit -m "feat: add install/deploy script"
```

**Verify**: `git log --oneline -1` shows the commit message.

## Test plan

No formal test framework. Manual verification:
1. `bash scripts/install.sh --help` — prints usage, exits 0
2. `bash scripts/install.sh --dry-run` — prints copy commands, exits 0, no files actually copied
3. `bash scripts/install.sh --dry-run --uninstall` — prints removal commands, exits 0
4. `bash scripts/install.sh` — copies files to `~/.omp/agent/`, exits 0
5. `bash scripts/install.sh --uninstall` — removes files from `~/.omp/agent/`, exits 0
6. Re-install with `bash scripts/install.sh` (idempotency check)

## Done criteria

ALL must hold:

- [ ] `scripts/install.sh` exists and is executable
- [ ] `bash scripts/install.sh --help` exits 0 and prints usage
- [ ] `bash scripts/install.sh --dry-run` exits 0, prints planned actions, no files modified
- [ ] `bash scripts/install.sh` exits 0, files exist at `~/.omp/agent/APPEND_SYSTEM.md` and `~/.omp/agent/RULES.md`
- [ ] `bash scripts/install.sh --uninstall` exits 0, files removed from `~/.omp/agent/`
- [ ] `git status --short` is clean
- [ ] `plans/README.md` status row updated

## STOP conditions

Stop and report back (do not improvise) if:

- `scripts/` already exists with files that would conflict.
- `~/.omp/agent/` doesn't exist and the user doesn't have OMP installed — the script should handle this gracefully (create the dir), but if OMP itself isn't installed, note it.
- Any source config file listed in the plan has been removed or renamed.

## Maintenance notes

- When new deployable files are added to the repo, add corresponding install/uninstall steps.
- The script intentionally does NOT run `ollama create` — that's a separate concern with side effects (model download). Keep it documented in README as a manual step.
- Consider adding `--only-ollama` flag in the future to handle the `ollama create` step.
