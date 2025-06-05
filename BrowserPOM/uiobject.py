from __future__ import annotations

from typing import Self, Union

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

    def __getitem__(self, index: Union[int, str]) -> Self:
        """
        Retrieves an indexed or text-based child UI object.

        Args:
            index (Union[int, str]): The index or text value of the child UI object.

        Returns:
            UIObject: A new UIObject instance representing the indexed or text-based child.
        """
        if isinstance(index, int):
            # Handle numeric index
            return self.__class__(self.locator + f" >> nth={index}", parent=self.parent)
        if isinstance(index, str):
            # handle text directly as an appended locator
            if self.locator.startswith("css"):
                # If the locator is a CSS selector, we need to ensure it is properly formatted
                element = f"{self.locator}:has-text('{index}')"
            elif self.locator.startswith("xpath"):
                # If the locator is an XPath selector, we need to ensure it is properly formatted
                element = f"{self.locator}[contains(., '{index}')]"
            else:
                raise AttributeError(f"Locator '{self.locator}' must start with 'css=' or 'xpath=' to use text-based indexing.")
            return self.__class__(element, parent=self.parent)
        raise TypeError("Index must be an int or a str.")

    def self_locator(self) -> str:
        """
        Returns the locator string of the UI object without merging with parent.

        Returns:
            str: The locator string.
        """
        return self.locator

    def __str__(self) -> str:
        """
        Returns the string representation of the UI object.

        Returns:
            str: The locator string, including parent locators if applicable.
        """
        composite_locator = self.locator if self.parent is None else f"{self.parent} >> {self.locator}"
        print(composite_locator)
        return composite_locator
