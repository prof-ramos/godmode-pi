"""Install/uninstall logic for godmode-pi configs."""

import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
OMP_DIR = Path.home() / ".omp" / "agent"

CONFIG_FILES = ["APPEND_SYSTEM.md", "RULES.md", "config.yml"]


def _copy(src: Path, dst: Path, dry_run: bool) -> None:
    """Copy src to dst, backing up dst if it exists."""
    if dry_run:
        print(f"  [dry-run] cp {src} -> {dst}")
        if dst.exists():
            print(f"  [dry-run] (backup existing {dst} to {dst}.bak)")
        return
    if dst.exists():
        backup = dst.with_suffix(dst.suffix + ".bak")
        shutil.copy2(dst, backup)
        print(f"  Backed up {dst} to {backup}")
    shutil.copy2(src, dst)
    print(f"  Installed {dst}")


def _remove(path: Path, dry_run: bool) -> None:
    """Remove path if it exists."""
    if not path.exists():
        return
    if dry_run:
        print(f"  [dry-run] rm {path}")
        return
    path.unlink()
    print(f"  Removed {path}")


def install(dry_run: bool = False) -> None:
    """Install config files to ~/.omp/agent/."""
    print("Installing godmode-pi...")
    if dry_run:
        print(f"  [dry-run] mkdir -p {OMP_DIR}")
    else:
        OMP_DIR.mkdir(parents=True, exist_ok=True)

    for name in CONFIG_FILES:
        src = REPO_ROOT / name
        if not src.exists():
            print(f"  ERROR: {src} not found")
            continue
        dst = OMP_DIR / name
        _copy(src, dst, dry_run)

    print("Install complete")


def uninstall(dry_run: bool = False) -> None:
    """Remove installed config files from ~/.omp/agent/."""
    print("Uninstalling godmode-pi...")
    for name in CONFIG_FILES:
        dst = OMP_DIR / name
        _remove(dst, dry_run)
    print("Uninstall complete")


def status() -> list[tuple[str, bool]]:
    """Check which configs are installed."""
    results: list[tuple[str, bool]] = []
    for name in CONFIG_FILES:
        dst = OMP_DIR / name
        results.append((name, dst.exists()))
    return results
