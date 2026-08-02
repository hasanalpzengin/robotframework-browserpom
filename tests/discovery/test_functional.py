"""Functional tests for `browserpom discover pages` / `discover objects`.

Each subdirectory under `functional/pages/` or `functional/objects/` is a
self-contained case: a `pyproject.toml`, POM source files, and an
`expected_output.txt` holding the exact stdout the discovery command must
produce when run with that directory as the project root.

Adding a new case means adding a new subdirectory — no test code required.
"""

# ruff: noqa

from __future__ import annotations

import io
from contextlib import redirect_stdout
from pathlib import Path

import pytest
from BrowserPOM.cli.cli import build_parser, cmd_discover_objects, cmd_discover_pages

FUNCTIONAL_ROOT = Path(__file__).parent / "functional"


def _discover_cases(bucket: str) -> list[Path]:
    """Find every case directory under a bucket, at any nesting depth.

    A case directory is identified by containing a `pyproject.toml` —
    cases may be grouped into category subdirectories (e.g.
    `objects/properties/dunder_property_excluded/`) purely for readability;
    the category folder itself is not a case.
    """
    bucket_dir = FUNCTIONAL_ROOT / bucket
    return sorted(p.parent for p in bucket_dir.rglob("pyproject.toml"))


def _run_case(case_dir: Path, args, cmd, monkeypatch: pytest.MonkeyPatch) -> str:
    monkeypatch.chdir(case_dir)
    buf = io.StringIO()
    with redirect_stdout(buf):
        cmd(args)
    return buf.getvalue()


@pytest.mark.parametrize(
    "case_dir",
    _discover_cases("pages"),
    ids=lambda p: str(p.relative_to(FUNCTIONAL_ROOT / "pages")),
)
def test_pages_case(case_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    args = build_parser().parse_args(["discover", "pages"])
    actual = _run_case(case_dir, args, cmd_discover_pages, monkeypatch)
    expected = (case_dir / "expected_output.txt").read_text()
    assert actual.rstrip() == expected.rstrip()


@pytest.mark.parametrize(
    "case_dir",
    _discover_cases("objects"),
    ids=lambda p: str(p.relative_to(FUNCTIONAL_ROOT / "objects")),
)
def test_objects_case(case_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    args = build_parser().parse_args(["discover", "objects"])
    actual = _run_case(case_dir, args, cmd_discover_objects, monkeypatch)
    expected = (case_dir / "expected_output.txt").read_text()
    assert actual.rstrip() == expected.rstrip()
