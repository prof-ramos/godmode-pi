"""CLI entry point for godmode-pi."""

import argparse
import sys

from godmode_pi import __version__
from godmode_pi.validate import validate_all
from godmode_pi.install import install, uninstall, status


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="godmode-pi",
        description="Validate and install godmode-pi jailbreak configs",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"godmode-pi {__version__}",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    # validate
    val_parser = sub.add_parser("validate", help="Validate config files")
    val_parser.add_argument(
        "--files",
        nargs="*",
        default=None,
        help="Specific files to validate (default: all known configs)",
    )

    # install
    inst_parser = sub.add_parser("install", help="Install configs to ~/.omp/agent/")
    inst_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be done without modifying files",
    )
    inst_parser.add_argument(
        "--uninstall",
        action="store_true",
        help="Remove installed files",
    )

    # status
    sub.add_parser("status", help="Show installation status")

    args = parser.parse_args(argv)

    if args.command == "validate":
        results = validate_all(files=args.files)
        all_ok = True
        for path, ok, msg in results:
            status_str = "OK" if ok else "INVALID"
            print(f"{path}: {status_str} — {msg}")
            if not ok:
                all_ok = False
        if all_ok:
            print("All configs valid")
        else:
            sys.exit(1)

    elif args.command == "install":
        if args.uninstall:
            uninstall(dry_run=args.dry_run)
        else:
            install(dry_run=args.dry_run)

    elif args.command == "status":
        results = status()
        for path, installed in results:
            s = "installed" if installed else "not installed"
            print(f"{path}: {s}")


if __name__ == "__main__":
    main()
