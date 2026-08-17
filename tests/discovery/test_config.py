# ruff: noqa
"""Tests for [tool.browserpom.discover] config loading and validation."""

import pytest
from BrowserPOM.cli.cli import build_parser, cmd_discover_pages, cmd_discover_objects
from BrowserPOM.cli.exceptions import ConfigError, DiscoveryError


def _pages_args():
    return build_parser().parse_args(["discover", "pages"])


def _objects_args():
    return build_parser().parse_args(["discover", "objects"])


class TestMissingConfig:
    def test_no_pyproject_toml_raises_config_error(self, tmp_path, monkeypatch):
        """Running from a directory with no pyproject.toml is a ConfigError."""
        monkeypatch.chdir(tmp_path)
        with pytest.raises(ConfigError, match="No pyproject.toml found"):
            cmd_discover_pages(_pages_args())

    def test_missing_discover_section_raises_config_error(self, tmp_path, monkeypatch):
        """A pyproject.toml with no [tool.browserpom.discover] section is a ConfigError."""
        (tmp_path / "pyproject.toml").write_text("[project]\nname = 'test'\n")
        monkeypatch.chdir(tmp_path)
        with pytest.raises(ConfigError, match=r"\[tool\.browserpom\.discover\]"):
            cmd_discover_pages(_pages_args())


class TestEmptyConfig:
    def test_empty_paths_raises_config_error(self, tmp_path, monkeypatch):
        """An explicitly empty paths list counts as no scan targets."""
        (tmp_path / "pyproject.toml").write_text("[tool.browserpom.discover]\n")
        monkeypatch.chdir(tmp_path)
        with pytest.raises(ConfigError, match="at least one entry"):
            cmd_discover_pages(_pages_args())

    def test_paths_only_is_valid(self, tmp_path, monkeypatch):
        """A single paths entry is sufficient — no ConfigError."""
        (tmp_path / "src").mkdir()
        (tmp_path / "pyproject.toml").write_text("[tool.browserpom.discover]\npaths = ['src/']\n")
        monkeypatch.chdir(tmp_path)
        cmd_discover_pages(_pages_args())  # must not raise


class TestMalformedConfig:
    def test_malformed_paths_raises_config_error(self, tmp_path, monkeypatch):
        """paths must be a list; a scalar value raises ConfigError."""
        (tmp_path / "pyproject.toml").write_text("[tool.browserpom.discover]\npaths = 'not-a-list'\n")
        monkeypatch.chdir(tmp_path)
        with pytest.raises(ConfigError, match="'paths' must be a list"):
            cmd_discover_pages(_pages_args())


class TestMissingScanPath:
    def test_missing_path_raises_discovery_error(self, tmp_path, monkeypatch):
        """A configured path that does not exist raises DiscoveryError."""
        (tmp_path / "pyproject.toml").write_text("[tool.browserpom.discover]\npaths = ['missing/']\n")
        monkeypatch.chdir(tmp_path)
        with pytest.raises(DiscoveryError, match="missing/"):
            cmd_discover_objects(_objects_args())

    def test_missing_path_via_main_exits_with_code_1(self, tmp_path, monkeypatch):
        """A DiscoveryError from a missing path becomes SystemExit(1) in main()."""
        from BrowserPOM.cli.cli import main

        (tmp_path / "pyproject.toml").write_text("[tool.browserpom.discover]\npaths = ['missing/']\n")
        monkeypatch.chdir(tmp_path)
        with pytest.raises(SystemExit) as exc_info:
            main(["discover", "objects"])
        assert exc_info.value.code == 1


class TestMainIntegration:
    def test_config_error_becomes_system_exit_via_main(self, tmp_path, monkeypatch):
        """main() converts ConfigError to SystemExit(1)."""
        from BrowserPOM.cli.cli import main

        monkeypatch.chdir(tmp_path)
        with pytest.raises(SystemExit) as exc_info:
            main(["discover", "pages"])
        assert exc_info.value.code == 1
