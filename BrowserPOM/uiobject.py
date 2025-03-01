from __future__ import annotations
from typing import Self

from Browser import Browser
from robot.libraries.BuiltIn import BuiltIn


class UIObject:
    def __init__(self, parent: UIObject | None, locator: str) -> None:
        self.parent = parent
        self.locator = locator
        self.index: int | None = None

    @property
    def browser(self) -> Browser:
        return BuiltIn().get_library_instance("Browser")

    def __getitem__(self, index: int) -> Self:
        self.index = index
        return self

    def __str__(self) -> str:
        locator = self.locator + f"[{self.index}]" if self.index is not None else self.locator
        if self.parent:
            locator = f"{self.parent} >> {locator}"
        return locator
