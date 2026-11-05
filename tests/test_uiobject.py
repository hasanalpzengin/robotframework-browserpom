"""Tests for UIObject's Python protocols."""

# ruff: noqa: S101

from unittest.mock import Mock, patch

import pytest
from BrowserPOM.uiobject import UIObject
from robot.variables import Variables


class Row(UIObject):
    """A UIObject with its own behavior and a nested UIObject attribute."""

    def __init__(self, locator: str, parent: UIObject | None = None) -> None:
        """Create a row and its label."""
        super().__init__(locator, parent)
        self.label = UIObject(".label", parent=self)

    def label_locator(self) -> str:
        """Expose behavior available only on this subclass."""
        return str(self.label)


@pytest.fixture
def browser(monkeypatch: pytest.MonkeyPatch) -> Mock:
    """Replace the Robot-managed Browser connection."""
    instance = Mock()
    monkeypatch.setattr(UIObject, "browser", property(lambda _self: instance))
    return instance


@pytest.mark.parametrize("count", [0, 1, 3])
@pytest.mark.parametrize("object_type", [UIObject, Row])
def test_iteration_matches_indexing(browser: Mock, count: int, object_type: type[UIObject]) -> None:
    """Yield exactly the matches as typed, parent-preserving indexed UIObjects."""
    browser.get_element_count.return_value = count
    parent = UIObject("#table", parent=UIObject("#container"))
    rows = object_type(".row", parent=parent)

    matches = list(rows)

    browser.get_element_count.assert_called_once_with("#container >> #table >> .row")
    assert len(matches) == count
    for index, match in enumerate(matches):
        assert type(match) is object_type
        assert match is not rows
        assert match.parent is parent
        assert str(match) == str(rows[index])
        if isinstance(match, Row):
            assert match.label.parent is match
            assert match.label_locator() == f"{rows[index]} >> .label"


def test_python_for_loop_without_parent(browser: Mock) -> None:
    """A regular Python loop visits all matches in order."""
    browser.get_element_count.return_value = 2
    locators = []
    for match in UIObject(".row", parent=None):
        locators.append(str(match))  # noqa: PERF401 - Exercise a Python for loop explicitly.
    assert locators == [".row >> nth=0", ".row >> nth=1"]
    browser.get_element_count.assert_called_once_with(".row")


def test_independent_iterations_recount_matches(browser: Mock) -> None:
    """Each iterator counts once and retains its own range while being consumed."""
    counts = [2, 1, 0]
    browser.get_element_count.side_effect = counts
    rows = UIObject(".row")
    first = iter(rows)
    assert str(next(first)) == ".row >> nth=0"
    assert [str(row) for row in rows] == [".row >> nth=0"]
    assert [str(row) for row in first] == [".row >> nth=1"]
    assert list(rows) == []
    assert browser.get_element_count.call_count == len(counts)


def test_iteration_propagates_browser_error(browser: Mock) -> None:
    """A count failure must not look like an empty collection."""
    browser.get_element_count.side_effect = RuntimeError("Browser unavailable")
    with pytest.raises(RuntimeError, match="Browser unavailable"):
        list(UIObject(".row"))


@pytest.mark.parametrize("count", [0, 1, 3])
def test_robot_list_expansion(browser: Mock, count: int) -> None:
    """Robot's real variable resolver expands UIObject attributes into typed items."""
    browser.get_element_count.return_value = count
    variables = Variables()
    page = Mock()
    page.rows = Row(".row", parent=UIObject("#table"))
    variables["${MyPage}"] = page

    matches = variables.replace_list(["@{MyPage.rows}"])

    assert [str(match) for match in matches] == [f"#table >> .row >> nth={index}" for index in range(count)]
    assert all(isinstance(match, Row) for match in matches)
    browser.get_element_count.assert_called_once_with("#table >> .row")


def test_membership_tests_are_not_supported() -> None:
    """Membership tests must raise TypeError instead of iterating indefinitely."""
    obj = UIObject("div")

    with patch.object(
        UIObject,
        "__getitem__",
        side_effect=AssertionError("Membership test attempted indexed iteration"),
    ):
        with pytest.raises(TypeError, match="does not support membership tests"):
            _ = "test" in obj

        with pytest.raises(TypeError, match="does not support membership tests"):
            _ = "test" not in obj
