# ruff: noqa
"""Unit tests for relative-import resolution in `BrowserPOM.cli.scanner`.

Exercises `Scanner.scan()` (the public API) directly rather than the fixture-based
functional harness, so the assertions can inspect specific classes/children without
depending on file-iteration order for a full expected-output comparison. Indexing is a
pure performance change with no observable behavior difference, so it isn't covered by
a dedicated test here — the existing discovery test suite staying green is its regression
coverage, per the originating ticket.
"""

from pathlib import Path

from BrowserPOM.cli.scanner import Scanner


class TestScannerRelativeImports:
    def _write(self, root: Path, rel_path: str, content: str) -> None:
        path = root / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    def test_exact_match_wins_over_short_name_ambiguity(self, tmp_path):
        """A relatively-imported base/child type must resolve to its exact fully-qualified
        match, not fall back to (possibly ambiguous) short-name matching against a same-named
        decoy class defined elsewhere.
        """
        root = tmp_path
        self._write(
            root,
            "app/component/shared/base.py",
            "from BrowserPOM.uiobject import UIObject\n\nclass SharedBase(UIObject):\n    marker = UIObject('css=.real-marker')\n",
        )
        # Decoy: same short name, different package, different content.
        self._write(
            root,
            "app/other/decoy.py",
            "from BrowserPOM.uiobject import UIObject\n\nclass SharedBase(UIObject):\n    decoy_marker = UIObject('css=.decoy-marker')\n",
        )
        self._write(
            root,
            "app/component/deep/deep_child.py",
            "from ..shared.base import SharedBase\n\nclass DeepChild(SharedBase):\n    shared_child = SharedBase('css=.deep-shared-child')\n",
        )

        scanner = Scanner(root, ["."])
        classes = scanner.scan()
        by_name_and_file = {(c.name, c.file_path): c for c in classes}

        deep_child = by_name_and_file[("DeepChild", root / "app/component/deep/deep_child.py")]
        assert len(deep_child.children) == 1
        shared_child = deep_child.children[0]
        assert shared_child.type_name == "SharedBase"
        # Resolved from the real SharedBase (has `marker`), not the decoy (`decoy_marker`).
        assert [c.name for c in shared_child.children] == ["marker"]

    def test_zero_dot_relative_import_from_package_init(self, tmp_path):
        root = tmp_path
        self._write(
            root,
            "app/__init__.py",
            "from BrowserPOM.uiobject import UIObject\n\nclass DirectBase(UIObject):\n    pass\n",
        )
        self._write(
            root,
            "app/direct_child.py",
            "from . import DirectBase\n\nclass DirectChild(DirectBase):\n    pass\n",
        )

        scanner = Scanner(root, ["."])
        names = {c.name for c in scanner.scan()}
        assert {"DirectBase", "DirectChild"} <= names

    def test_one_dot_relative_import_from_subpackage(self, tmp_path):
        root = tmp_path
        self._write(
            root,
            "app/subpkg/__init__.py",
            "from BrowserPOM.uiobject import UIObject\n\nclass SubBase(UIObject):\n    pass\n",
        )
        self._write(
            root,
            "app/subpkg_child.py",
            "from .subpkg import SubBase\n\nclass SubpkgChild(SubBase):\n    pass\n",
        )

        scanner = Scanner(root, ["."])
        names = {c.name for c in scanner.scan()}
        assert {"SubBase", "SubpkgChild"} <= names

    def test_multi_dot_relative_import_across_packages(self, tmp_path):
        root = tmp_path
        self._write(
            root,
            "app/component/shared/base.py",
            "from BrowserPOM.uiobject import UIObject\n\nclass SharedBase(UIObject):\n    pass\n",
        )
        self._write(
            root,
            "app/component/deep/deep_child.py",
            "from ..shared.base import SharedBase\n\nclass DeepChild(SharedBase):\n    pass\n",
        )

        scanner = Scanner(root, ["."])
        names = {c.name for c in scanner.scan()}
        assert {"SharedBase", "DeepChild"} <= names
