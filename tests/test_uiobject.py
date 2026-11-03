"""Tests for UIObject's Python protocols."""

from unittest.mock import patch

import pytest
from BrowserPOM.uiobject import UIObject


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
