from __future__ import annotations
from typing import Self

from Browser import Browser
from robot.libraries.BuiltIn import BuiltIn


class UIObject:
    def __init__(self, parent: UIObject | None, locator: str) -> None:
        self.parent = parent
        self.locator = locator

    @property
    def browser(self) -> Browser:
        return BuiltIn().get_library_instance("Browser")

    def __getitem__(self, index: int) -> Self:
        return self.__class__(parent=self.parent, locator=self.locator + f">> nth={index}")

    def __str__(self) -> str:
        return self.locator if self.parent is None else f"{self.parent} >> {self.locator}"
