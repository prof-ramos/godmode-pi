"""Config file validation logic."""

import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent

KNOWN_CONFIGS: list[str] = [
    "config.yml",
    "prefill.json",
    "Modelfile-godmode",
    "APPEND_SYSTEM.md",
    "RULES.md",
]


def validate_config_yml(path: Path) -> tuple[bool, str]:
    """Validate config.yml has a systemPrompt key with a list of strings."""
    try:
        content = path.read_text()
        assert re.search(r"^\w+:", content, re.MULTILINE), "no top-level key found"
        assert "systemPrompt" in content, "missing systemPrompt key"
        return True, "OK (basic structure)"
    except Exception as e:
        return False, str(e)


def validate_prefill_json(path: Path) -> tuple[bool, str]:
    """Validate prefill.json is an array of {role, content} objects."""
    try:
        data = json.loads(path.read_text())
        assert isinstance(data, list), "root must be an array"
        for i, msg in enumerate(data):
            assert "role" in msg, f"[{i}]: missing role"
            assert msg["role"] in ("user", "assistant"), f"[{i}]: role must be user/assistant"
            assert "content" in msg, f"[{i}]: missing content"
            assert isinstance(msg["content"], str), f"[{i}]: content must be string"
        return True, "OK"
    except Exception as e:
        return False, str(e)


def validate_modelfile(path: Path) -> tuple[bool, str]:
    """Validate Modelfile-godmode has FROM and SYSTEM directives."""
    try:
        content = path.read_text()
        lines = content.splitlines()
        has_from = any(line.startswith("FROM") for line in lines)
        has_system = any(line.startswith("SYSTEM") for line in lines)
        if not has_from:
            return False, "missing FROM directive"
        if not has_system:
            return False, "missing SYSTEM directive"
        return True, "OK"
    except Exception as e:
        return False, str(e)


def validate_markdown(path: Path) -> tuple[bool, str]:
    """Validate a Markdown file is non-empty."""
    try:
        size = path.stat().st_size
        if size == 0:
            return False, "empty file"
        return True, "OK"
    except Exception as e:
        return False, str(e)


VALIDATORS: dict[str, callable] = {
    "config.yml": validate_config_yml,
    "prefill.json": validate_prefill_json,
    "Modelfile-godmode": validate_modelfile,
    "APPEND_SYSTEM.md": validate_markdown,
    "RULES.md": validate_markdown,
}


def validate_all(files: list[str] | None = None) -> list[tuple[str, bool, str]]:
    """Validate config files. Returns list of (filename, ok, message)."""
    if files is None:
        files = KNOWN_CONFIGS

    results: list[tuple[str, bool, str]] = []
    for name in files:
        path = REPO_ROOT / name
        if not path.exists():
            results.append((name, False, "file not found"))
            continue
        validator = VALIDATORS.get(name)
        if validator is None:
            results.append((name, False, f"no validator for {name}"))
            continue
        ok, msg = validator(path)
        results.append((name, ok, msg))
    return results
