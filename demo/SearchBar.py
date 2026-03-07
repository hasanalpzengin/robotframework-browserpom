"""Demo search bar object."""

from BrowserPOM.uiobject import UIObject


class SearchBar(UIObject):
    """Represents the search bar in the demo page."""

    def __init__(self, locator: str, parent: UIObject | None = None) -> None:
        """Initialize the search bar locator."""
        super().__init__(locator, parent=parent)

    def search(self, text: str) -> None:
        """Search for the given text in the search bar."""
        self.browser.type_text(str(self), text)
