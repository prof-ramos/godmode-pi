#!/usr/bin/env bash
set -euo pipefail

OMP_DIR="$HOME/.omp/agent"
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"

usage() {
    cat <<EOF
Usage: $(basename "$0") [OPTION]

Install or uninstall godmode-pi configuration files.

Options:
  --dry-run    Print what would be done without modifying files
  --uninstall  Remove installed files (reverse of install)
  --help       Print this usage message

Without options, installs config files to $OMP_DIR
EOF
    exit 0
}

DRY_RUN=false
UNINSTALL=false

for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=true ;;
        --uninstall) UNINSTALL=true ;;
        --help) usage ;;
        *) echo "Unknown option: $arg"; usage ;;
    esac
done

if $UNINSTALL; then
    echo "Uninstalling godmode-pi..."
    for f in APPEND_SYSTEM.md RULES.md; do
        target="$OMP_DIR/$f"
        if [ -f "$target" ]; then
            if $DRY_RUN; then
                echo "  [dry-run] rm $target"
            else
                rm "$target"
                echo "  Removed $target"
            fi
        else
            echo "  (not installed) $target"
        fi
    done
    echo "Uninstall complete"
    exit 0
fi

echo "Installing godmode-pi..."

# Ensure target directory exists
if $DRY_RUN; then
    echo "  [dry-run] mkdir -p $OMP_DIR"
else
    mkdir -p "$OMP_DIR"
fi

# Copy primary config files
for f in APPEND_SYSTEM.md RULES.md; do
    src="$REPO_DIR/$f"
    target="$OMP_DIR/$f"
    if [ ! -f "$src" ]; then
        echo "  ERROR: $src not found (run from repo root)"
        exit 1
    fi
    if $DRY_RUN; then
        echo "  [dry-run] cp $src -> $target"
    else
        cp "$src" "$target"
        echo "  Installed $target"
    fi
done

# Copy config.yml with backup
src="$REPO_DIR/config.yml"
target="$OMP_DIR/config.yml"
if [ -f "$src" ]; then
    if $DRY_RUN; then
        echo "  [dry-run] cp $src -> $target"
        if [ -f "$target" ]; then
            echo "  [dry-run] (backup existing $target to ${target}.bak)"
        fi
    else
        if [ -f "$target" ]; then
            cp "$target" "${target}.bak"
            echo "  Backed up existing config.yml to config.yml.bak"
        fi
        cp "$src" "$target"
        echo "  Installed $target"
    fi
fi

echo "Install complete"
