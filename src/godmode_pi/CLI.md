# CLI API Design

## Commands

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

## Implementation

- `argparse`-based CLI with subcommands
- Each subcommand is a function in its own module
- Validation logic mirrors `scripts/validate.sh` but in Python
- Install logic mirrors `scripts/install.sh` but in Python
