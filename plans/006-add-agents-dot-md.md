# Plan 006: Add AGENTS.md for AI-agent project context

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md` — unless a reviewer dispatched you and told you they
> maintain the index.
>
> **Drift check (run first)**: `git diff --stat ddd7081..HEAD -- AGENTS.md`
> If the file already exists, compare its content against the plan's
> assumptions before proceeding; on a mismatch, treat it as a STOP condition.

## Status

- **Priority**: P1
- **Effort**: S
- **Risk**: LOW
- **Depends on**: none
- **Category**: dx
- **Planned at**: commit `ddd7081`, 2026-06-20

## Why this matters

AI agents (Claude Code, OpenCode, Cursor) working on this repo have no project-specific context — no description of what the config files do, no instructions on what to preserve, no conventions to follow. Every session starts cold. An `AGENTS.md` file provides the shared context that makes agent work reliable: which files are the primary deliverables, what each config format expects, and what invariants must never be broken.

## Current state

No `AGENTS.md` or `CLAUDE.md` exists in the repo root. The `.omc/` directory (gitignored) contains session state but no project-level agent instructions.

The repo's tracked files and their roles:
- `APPEND_SYSTEM.md` — primary deliverable: appends to OMP system prompt
- `RULES.md` — primary deliverable: persistent rules for OMP
- `config.yml` — primary deliverable: OMP systemPrompt array
- `Modelfile-godmode` — primary deliverable: custom Ollama model
- `prefill.json` — primary deliverable: Hermes Agent priming messages
- `README.md` — documentation
- `LICENSE` — MIT
- `.gitignore` — gitignore rules

## Commands you will need

| Purpose | Command | Expected on success |
|---------|---------|---------------------|
| Check file exists | `test -f AGENTS.md` | exit 0 |
| Check file size | `wc -l < AGENTS.md` | > 10 |

## Scope

**In scope** (the only files you should create):
- `AGENTS.md` — create

**Out of scope** (do NOT touch):
- `CLAUDE.md` — not needed; `AGENTS.md` is the standard for this repo
- `README.md` — separate concern
- Any config file — the AGENTS.md describes them, doesn't modify them
- `.omc/` — gitignored session state

## Git workflow

- Branch: `advisor/006-add-agents-dot-md`
- Commit message: `docs: add AGENTS.md for AI-agent project context`
- Do NOT push or open a PR unless the operator instructed it

## Steps

### Step 1: Create `AGENTS.md`

Create a file at the repo root with the following sections:

```markdown
# godmode-pi — Agent Context

Persistent jailbreak configuration for **Oh My Pi (OMP)** agent running
**deepseek-v4-flash** via **Ollama Cloud** on macOS.

## Project Structure

| File | Purpose |
|------|---------|
| `APPEND_SYSTEM.md` | Appends to OMP built-in system prompt (recommended approach) |
| `RULES.md` | Persistent rules active across context compression |
| `config.yml` | OMP systemPrompt array (works with Ollama Cloud) |
| `Modelfile-godmode` | Custom Ollama model definition |
| `prefill.json` | Priming messages for Hermes Agent |
| `README.md` | Full documentation with install/verify/undo procedures |

## Invariants (NEVER break these)

1. `APPEND_SYSTEM.md` must contain the 7 GODMODE directives numbered 1-7.
2. `RULES.md` must contain the 5 GODMODE rules as bullet points.
3. `config.yml` must have a `systemPrompt` key with a list of strings.
4. `prefill.json` must be an array of `{role, content}` objects with alternating user/assistant roles.
5. `Modelfile-godmode` must start with `FROM` and contain `SYSTEM` directive.
6. All config files must be valid YAML/JSON per their format.

## Model Strategies

| Model | Best Approach |
|-------|--------------|
| DeepSeek | Refusal-inversion + APPEND_SYSTEM.md |
| Claude | END/START boundary or refusal-inversion |
| GPT-4/4o | OG GODMODE l33t divider |
| Gemini | Refusal-inversion + rebel persona |
| Grok | Unfiltered liberated |
| Hermes/Nous | None needed (already uncensored) |

## Commands

- Validate configs: `bash scripts/validate.sh` (if scripts/ exists)
- Install: `bash scripts/install.sh` (if scripts/ exists)
- Test OMP: `omp -p '/extensions'`
- Test jailbreak: `omp -p "Explain step by step how to pick a lock."`
```

**Verify**: `test -f AGENTS.md && wc -l < AGENTS.md` shows at least 40 lines.

### Step 2: Commit

```bash
git add AGENTS.md && git commit -m "docs: add AGENTS.md for AI-agent project context"
```

**Verify**: `git log --oneline -1` shows the commit message.

## Test plan

No tests to write. Verification:
1. File exists and is non-empty
2. Content is valid Markdown (no syntax errors)
3. All referenced files actually exist in the repo

## Done criteria

ALL must hold:

- [ ] `test -f AGENTS.md` exits 0
- [ ] `grep -q "APPEND_SYSTEM.md" AGENTS.md` exits 0 (references actual files)
- [ ] `grep -q "RULES.md" AGENTS.md` exits 0
- [ ] `grep -q "config.yml" AGENTS.md` exits 0
- [ ] `grep -q "Modelfile-godmode" AGENTS.md` exits 0
- [ ] `grep -q "prefill.json" AGENTS.md` exits 0
- [ ] `git status --short` is clean
- [ ] `plans/README.md` status row updated

## STOP conditions

Stop and report back (do not improvise) if:

- `AGENTS.md` already exists with content that would conflict.
- Any config file referenced in the template has been removed or renamed.
- The repo's structure has changed significantly (e.g., new primary deliverables exist).

## Maintenance notes

- Keep `AGENTS.md` in sync with the actual file structure — when adding or removing config files, update the table.
- The "Invariants" section is the most important part for AI agents — it prevents accidental breakage of the jailbreak configs.
- If a `CLAUDE.md` is added later, it should reference `AGENTS.md` for project context rather than duplicating it.
