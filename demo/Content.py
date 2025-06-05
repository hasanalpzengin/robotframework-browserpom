from BrowserPOM.uiobject import UIObject
from demo.Tile import Tile


class Content(UIObject):
    def __init__(self, locator: str, parent: UIObject | None = None):
        super().__init__(locator, parent=parent)
        self.tile = Tile("xpath=//li", parent=self)