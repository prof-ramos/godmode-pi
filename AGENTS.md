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
