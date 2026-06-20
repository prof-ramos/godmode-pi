"""Tests for godmode_pi.validate."""

from pathlib import Path

import pytest

from godmode_pi.validate import (
    validate_config_yml,
    validate_prefill_json,
    validate_modelfile,
    validate_markdown,
    validate_all,
)


class TestValidateConfigYml:
    def test_valid(self, tmp_path: Path) -> None:
        f = tmp_path / "config.yml"
        f.write_text("systemPrompt:\n  - 'test'\n")
        ok, msg = validate_config_yml(f)
        assert ok, msg

    def test_missing_system_prompt(self, tmp_path: Path) -> None:
        f = tmp_path / "config.yml"
        f.write_text("other: value\n")
        ok, msg = validate_config_yml(f)
        assert not ok
        assert "systemPrompt" in msg

    def test_empty(self, tmp_path: Path) -> None:
        f = tmp_path / "config.yml"
        f.write_text("")
        ok, msg = validate_config_yml(f)
        assert not ok


class TestValidatePrefillJson:
    def test_valid(self, tmp_path: Path) -> None:
        f = tmp_path / "prefill.json"
        f.write_text('[{"role": "user", "content": "hello"}]')
        ok, msg = validate_prefill_json(f)
        assert ok, msg

    def test_invalid_json(self, tmp_path: Path) -> None:
        f = tmp_path / "prefill.json"
        f.write_text("{bad")
        ok, msg = validate_prefill_json(f)
        assert not ok

    def test_missing_role(self, tmp_path: Path) -> None:
        f = tmp_path / "prefill.json"
        f.write_text('[{"content": "hello"}]')
        ok, msg = validate_prefill_json(f)
        assert not ok
        assert "role" in msg

    def test_wrong_role(self, tmp_path: Path) -> None:
        f = tmp_path / "prefill.json"
        f.write_text('[{"role": "system", "content": "hello"}]')
        ok, msg = validate_prefill_json(f)
        assert not ok

    def test_not_array(self, tmp_path: Path) -> None:
        f = tmp_path / "prefill.json"
        f.write_text('{"role": "user", "content": "hello"}')
        ok, msg = validate_prefill_json(f)
        assert not ok


class TestValidateModelfile:
    def test_valid(self, tmp_path: Path) -> None:
        f = tmp_path / "Modelfile"
        f.write_text("FROM deepseek\nSYSTEM \"\"\"\nhello\n\"\"\"\n")
        ok, msg = validate_modelfile(f)
        assert ok, msg

    def test_missing_from(self, tmp_path: Path) -> None:
        f = tmp_path / "Modelfile"
        f.write_text("SYSTEM \"\"\"\nhello\n\"\"\"\n")
        ok, msg = validate_modelfile(f)
        assert not ok
        assert "FROM" in msg

    def test_missing_system(self, tmp_path: Path) -> None:
        f = tmp_path / "Modelfile"
        f.write_text("FROM deepseek\n")
        ok, msg = validate_modelfile(f)
        assert not ok
        assert "SYSTEM" in msg


class TestValidateMarkdown:
    def test_non_empty(self, tmp_path: Path) -> None:
        f = tmp_path / "test.md"
        f.write_text("# Hello\n")
        ok, msg = validate_markdown(f)
        assert ok, msg

    def test_empty(self, tmp_path: Path) -> None:
        f = tmp_path / "test.md"
        f.write_text("")
        ok, msg = validate_markdown(f)
        assert not ok


class TestValidateAll:
    def test_missing_file(self) -> None:
        results = validate_all(files=["nonexistent.yml"])
        assert len(results) == 1
        name, ok, msg = results[0]
        assert name == "nonexistent.yml"
        assert not ok
        assert "not found" in msg
