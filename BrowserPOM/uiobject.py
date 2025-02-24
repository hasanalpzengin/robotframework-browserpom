from __future__ import annotations

from Browser import Browser
from robot.libraries.BuiltIn import BuiltIn


class UIObject:
    def __init__(self, parent: UIObject | None, locator: str, is_list: bool = False) -> None:
        self.parent = parent
        self.locator = locator
        self.is_list = is_list
        self.index: int | None = None

    @property
    def browser(self) -> Browser:
        return BuiltIn().get_library_instance("Browser")

    def __getitem__(self, index: int) -> UIObject:
        if not self.is_list:
            raise ValueError("Indexing only available if `is_list` is set!")
        self.index = index
        return self

    def __str__(self) -> str:
        locator = self.locator + f"[{self.index}]" if self.index is not None else self.locator
        if self.parent:
            locator = f"{self.parent} >> {locator}"
        return locator
