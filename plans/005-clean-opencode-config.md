# Plan 005: Remove duplicate MCP servers from project-level OpenCode config

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md` — unless a reviewer dispatched you and told you they
> maintain the index.
>
> **Drift check (run first)**: `git diff --stat ddd7081..HEAD -- .opencode/opencode.json`
> If the file changed since this plan was written, compare the excerpts below
> against the live code before proceeding; on a mismatch, treat it as a STOP
> condition.

## Status

- **Priority**: P2
- **Effort**: S
- **Risk**: LOW
- **Depends on**: none
- **Category**: tech-debt
- **Planned at**: commit `ddd7081`, 2026-06-20

## Why this matters

The project-level `.opencode/opencode.json` declares MCP servers (context7, github, websearch) that are already configured in the global `~/.config/opencode/opencode.json`. OpenCode merges project and global configs, so the project-level declarations are redundant. Worse, the Context7 API key is duplicated on disk in the project config — if the global key is rotated, the stale project key silently breaks the MCP connection. Removing the duplicate MCP section eliminates the maintenance burden and the duplicated credential.

## Current state

The project-level config at `.opencode/opencode.json` (lines 4-24):
```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "opencode/deepseek-v4-flash-free",
  "mcp": {
    "context7": {
      "type": "remote",
      "url": "https://mcp.context7.com/mcp",
      "enabled": true,
      "headers": {
        "CONTEXT7_API_KEY": "ctx7sk-..."
      }
    },
    "github": {
      "type": "local",
      "command": ["gh", "mcp", "serve"],
      "enabled": true
    },
    "websearch": {
      "type": "remote",
      "url": "https://mcp.exa.ai/mcp?tools=web_search_exa",
      "enabled": true,
      "oauth": false
    }
  },
  "permission": { ... },
  "agent": { ... }
}
```

The global config at `~/.config/opencode/opencode.json` already has all three MCP servers configured with the same settings. OpenCode's config merge means the project config only needs to specify things that differ from or add to the global config.

## Commands you will need

| Purpose | Command | Expected on success |
|---------|---------|---------------------|
| Validate JSON | `python3 -c "import json; json.load(open('.opencode/opencode.json'))"` | exit 0 |
| Check MCP section | `grep -c '"mcp"' .opencode/opencode.json` | 0 (after removal) |

## Scope

**In scope** (the only files you should modify):
- `.opencode/opencode.json` — remove the `mcp` section

**Out of scope** (do NOT touch):
- The `permission` and `agent` sections — keep them as-is
- `~/.config/opencode/opencode.json` — global config, not part of this repo
- Any other file in the repo

## Git workflow

- Branch: `advisor/005-clean-opencode-config`
- Commit message: `chore: remove duplicate MCP servers from opencode config`
- Do NOT push or open a PR unless the operator instructed it

## Steps

### Step 1: Edit `.opencode/opencode.json`

Remove the `mcp` key and its entire value (lines 4-24). The file should become:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "opencode/deepseek-v4-flash-free",
  "permission": {
    "bash": {
      "gh *": "allow",
      "ollama *": "allow",
      "omp *": "allow",
      "hermes *": "allow"
    },
    "webfetch": "allow",
    "task": "allow"
  },
  "agent": {
    "GODMODE - Jailbreak Engineer": {
      ...
    }
  }
}
```

**Verify**: `python3 -c "import json; d=json.load(open('.opencode/opencode.json')); assert 'mcp' not in d; print('mcp removed: OK')"` exits 0.

### Step 2: Validate the JSON is well-formed

```bash
python3 -c "import json; json.load(open('.opencode/opencode.json')); print('valid JSON')"
```

**Verify**: Prints "valid JSON".

### Step 3: Commit

```bash
git add .opencode/opencode.json && git commit -m "chore: remove duplicate MCP servers from opencode config"
```

**Verify**: `git log --oneline -1` shows the commit message.

## Test plan

No tests to write. Verification:
1. The JSON is valid (step 2)
2. The `mcp` key is absent (step 1 verify)
3. The `permission` and `agent` sections are intact

## Done criteria

ALL must hold:

- [ ] `python3 -c "import json; d=json.load(open('.opencode/opencode.json')); assert 'mcp' not in d"` exits 0
- [ ] `python3 -c "import json; d=json.load(open('.opencode/opencode.json')); assert 'permission' in d and 'agent' in d"` exits 0
- [ ] `git status --short` is clean
- [ ] `plans/README.md` status row updated

## STOP conditions

Stop and report back (do not improvise) if:

- The `.opencode/opencode.json` structure differs from the excerpts (e.g., the `mcp` section was already removed by another plan).
- The `permission` or `agent` sections would be affected by the removal.
- The file is not valid JSON.

## Maintenance notes

- If a project-specific MCP server is needed in the future, add it back to the `mcp` section — but only for servers that aren't already in the global config.
- The `.opencode/` directory is gitignored, so this change only affects the local working copy. The config is personal to each developer's machine.
