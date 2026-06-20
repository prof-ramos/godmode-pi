"""Tests for godmode_pi.install."""

from pathlib import Path

import pytest

from godmode_pi.install import install, uninstall, status


class TestInstall:
    def test_dry_run_does_not_modify(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Dry-run should print actions but not create files."""
        omp_dir = tmp_path / ".omp" / "agent"
        monkeypatch.setattr("godmode_pi.install.OMP_DIR", omp_dir)

        install(dry_run=True)
        assert not omp_dir.exists(), "dry-run should not create directory"

    def test_install_creates_files(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        omp_dir = tmp_path / ".omp" / "agent"
        monkeypatch.setattr("godmode_pi.install.OMP_DIR", omp_dir)

        install(dry_run=False)
        assert omp_dir.exists()
        for name in ["APPEND_SYSTEM.md", "RULES.md", "config.yml"]:
            assert (omp_dir / name).exists(), f"{name} should exist"

    def test_uninstall_removes_files(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        omp_dir = tmp_path / ".omp" / "agent"
        monkeypatch.setattr("godmode_pi.install.OMP_DIR", omp_dir)

        install(dry_run=False)
        uninstall(dry_run=False)
        for name in ["APPEND_SYSTEM.md", "RULES.md", "config.yml"]:
            assert not (omp_dir / name).exists(), f"{name} should be removed"

    def test_status(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        omp_dir = tmp_path / ".omp" / "agent"
        monkeypatch.setattr("godmode_pi.install.OMP_DIR", omp_dir)

        # Before install — all not installed
        results = status()
        for _, installed in results:
            assert not installed

        # After install — all installed
        install(dry_run=False)
        results = status()
        for _, installed in results:
            assert installed
