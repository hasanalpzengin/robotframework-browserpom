from __future__ import annotations

from Browser import Browser
from robot.libraries.BuiltIn import BuiltIn


class UIObject:
    def __init__(self, parent: UIObject | None, locator: str) -> None:
        self.parent = parent
        self.locator = locator

    @property
    def browser(self) -> Browser:
        return BuiltIn().get_library_instance("Browser")

    def __str__(self) -> str:
        locator = self.locator
        if self.parent:
            locator = f"{self.parent} >> {locator}"
        return locator
