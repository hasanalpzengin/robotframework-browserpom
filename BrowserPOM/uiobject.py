"""Browser Page Object Model (POM) UIObject class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Self

from robot.libraries.BuiltIn import BuiltIn

if TYPE_CHECKING:
    from Browser import Browser


class UIObject:
    """Represents a UI object in the Browser Page Object Model (POM).

    Attributes:
        parent (UIObject | None): The parent UI object, or None if there is no parent.
        locator (str): The locator string used to identify the UI object.

    """

    def __init__(self, locator: str, parent: UIObject | None = None) -> None:
        """Initializes a UIObject instance.

        Args:
            parent (UIObject | None): The parent UI object, or None if there is no parent.
            locator (str): The locator string used to identify the UI object.

        """
        self.parent = parent
        self.locator = locator

    @property
    def browser(self) -> Browser:
        """Gets the Browser instance from Robot Framework's BuiltIn library.

        Returns:
            Browser: An instance of the Browser library.

        """
        return BuiltIn().get_library_instance("BrowserPOM")

    def __getitem__(self, index: int | str) -> Self:
        """Retrieves an indexed or text-based child UI object.

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
            return self.filter(f"hasText: '{index}'")
        raise TypeError("Index must be an int or a str.")

    def filter(self, filter_text: str) -> UIObject:
        """Filters the UI object by a given filter.

        See: https://playwright.dev/docs/locators#filtering-locators for more details

        Args:
            filter_text: The filter to apply to the UI object.

        Returns:
            UIObject: A new UIObject instance representing the filtered object.

        """
        base_locator = str(self).replace("'", '"')
        locator = BuiltIn().run_keyword(
            "Playwright Page Method",
            "locator('" + base_locator + "').filter({" + filter_text + "})",
        )
        return self.__class__(locator)

    def self_locator(self) -> str:
        """Returns the locator string of the UI object without merging with parent.

        Returns:
            str: The locator string.

        """
        return self.locator

    def __str__(self) -> str:
        """Returns the string representation of the UI object.

        Returns:
            str: The locator string, including parent locators if applicable.

        """
        return self.locator if self.parent is None else f"{self.parent} >> {self.locator}"
