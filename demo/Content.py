"""Demo content area object."""

from BrowserPOM.uiobject import UIObject

from demo.Tile import Tile


class Content(UIObject):
    """Represents the content section in the demo page."""

    def __init__(self, locator: str, parent: UIObject | None = None) -> None:
        """Initialize content area locators."""
        super().__init__(locator, parent=parent)
        self.tile = Tile("xpath=//li", parent=self)
