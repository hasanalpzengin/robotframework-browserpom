from __future__ import annotations

from typing import Self

from Browser import Browser
from robot.libraries.BuiltIn import BuiltIn


class UIObject:
    """
    Represents a UI object in the Browser Page Object Model (POM).

    Attributes:
        parent (UIObject | None): The parent UI object, or None if there is no parent.
        locator (str): The locator string used to identify the UI object.
    """

    def __init__(self, locator: str, parent: UIObject | None = None) -> None:
        """
        Initializes a UIObject instance.

        Args:
            parent (UIObject | None): The parent UI object, or None if there is no parent.
            locator (str): The locator string used to identify the UI object.
        """
        self.parent = parent
        self.locator = locator

    @property
    def browser(self) -> Browser:
        """
        Gets the Browser instance from Robot Framework's BuiltIn library.

        Returns:
            Browser: An instance of the Browser library.
        """
        return BuiltIn().get_library_instance("Browser")

    def __getitem__(self, index: int) -> Self:
        """
        Retrieves an indexed child UI object.

        Args:
            index (int): The index of the child UI object.

        Returns:
            UIObject: A new UIObject instance representing the indexed child.
        """
        return self.__class__(self.locator + f">> nth={index}", parent=self.parent)

    def __str__(self) -> str:
        """
        Returns the string representation of the UI object.

        Returns:
            str: The locator string, including parent locators if applicable.
        """
        return self.locator if self.parent is None else f"{self.parent} >> {self.locator}"
