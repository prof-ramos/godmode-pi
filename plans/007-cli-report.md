# CLI Tool Spike — Findings Report

## Summary

The Python CLI was prototyped successfully. All 18 tests pass, all 3
subcommands work (validate, install, status), and the tool mirrors the shell
scripts' behavior exactly.

## Is the Python CLI worth pursuing over shell scripts?

**Yes, but as a complement, not a replacement.** The shell scripts
(`scripts/validate.sh`, `scripts/install.sh`) are zero-dependency and work
anywhere. The Python CLI adds:

- **Structured output**: machine-parseable results (list of tuples)
- **Testability**: unit tests for validation logic
- **Extensibility**: easier to add new subcommands (e.g., `status`,
  `diff`, `backup`)
- **DX**: `--help`, `--version`, subcommand autocompletion

**Recommendation**: keep both. Shell scripts for CI and minimal
environments; Python CLI for interactive use and development.

## Key tradeoffs

| Aspect | Shell scripts | Python CLI |
|--------|--------------|------------|
| Dependencies | None | Python 3.10+, hatchling |
| Portability | Any POSIX | Requires Python + uv |
| Testability | Manual | pytest (18 tests) |
| Output format | Text | Structured (list of tuples) |
| Install size | ~2KB | ~10KB + Python runtime |
| CI integration | Direct | Requires `uv run` |

## Open questions

1. **Should `scripts/validate.sh` and `scripts/install.sh` be deprecated?**
   No — they serve CI and minimal environments. The Python CLI wraps the
   same logic but doesn't replace the shell scripts.

2. **Should the Python CLI be the primary interface?**
   Not yet. The shell scripts are simpler and more portable. If the repo
   grows more automation (e.g., model-specific deployment, A/B testing),
   the Python CLI becomes the natural home.

3. **Should we use `click` or `typer` instead of `argparse`?**
   `argparse` is stdlib and sufficient for 3 subcommands. If the CLI grows
   to 5+ subcommands or needs rich output, `typer` would improve DX.

## Effort estimate for production CLI

| Component | Effort | Notes |
|-----------|--------|-------|
| Current spike | S | Done — 3 subcommands, 18 tests |
| Add `--diff` subcommand | S | Compare repo configs vs installed |
| Add `--backup` / `--restore` | S | Snapshot/restore installed configs |
| Add model-specific deploy | M | `godmode-pi deploy --model deepseek` |
| Package for PyPI | S | Already has pyproject.toml |
| CI integration | S | `uv run godmode-pi validate` in CI |
