from BrowserPOM.uiobject import UIObject


class Tile(UIObject):
        def __init__(self, locator: str, parent: UIObject | None = None):
                super().__init__(locator, parent=parent)
                self.price = UIObject("//p[contains(@id, '_price')]", parent=self)
                self.title = UIObject("//h2[contains(@id, '_title')]", parent=self)
                self.author = UIObject("//p[contains(@id, '_author')]", parent=self)