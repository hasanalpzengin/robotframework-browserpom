"""Read and validate [tool.browserpom.discover] from pyproject.toml."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path

from BrowserPOM.cli.exceptions import ConfigError


@dataclass
class DiscoverConfig:
    """Validated contents of [tool.browserpom.discover]."""

    paths: list[str] = field(default_factory=list)


def load(project_root: Path | None = None) -> DiscoverConfig:
    """Load and validate [tool.browserpom.discover] from pyproject.toml.

    Args:
        project_root: Directory containing pyproject.toml.  Defaults to cwd.

    Returns:
        A DiscoverConfig with the configured paths.

    Raises:
        ConfigError: If pyproject.toml is missing, the [tool.browserpom.discover]
            section is absent, types are wrong, or no scan targets are configured.

    """
    root = project_root or Path.cwd()
    pyproject = root / "pyproject.toml"

    if not pyproject.exists():
        raise ConfigError(
            "No pyproject.toml found. Create one and add a [tool.browserpom.discover] section with 'paths'.",
        )

    with pyproject.open("rb") as fh:
        data = tomllib.load(fh)

    discover = data.get("tool", {}).get("browserpom", {}).get("discover")

    if discover is None:
        raise ConfigError(
            "No [tool.browserpom.discover] section found in pyproject.toml. Add 'paths' to configure discovery.",
        )

    paths = discover.get("paths", [])

    if not isinstance(paths, list):
        raise ConfigError(
            f"[tool.browserpom.discover] 'paths' must be a list, got {type(paths).__name__!r}",
        )

    if not paths:
        raise ConfigError(
            "[tool.browserpom.discover] requires at least one entry in 'paths'.",
        )

    return DiscoverConfig(paths=paths)
