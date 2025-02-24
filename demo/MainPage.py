from robot.api.deco import keyword

from BrowserPOM.pageobject import PageObject
from BrowserPOM.uiobject import UIObject


class Tile(UIObject):
    def __init__(self, parent: UIObject | None, locator: str) -> None:
        super().__init__(parent, locator)
        self.price_label = UIObject(parent=self, locator="//p[2]")
        self.title = UIObject(parent=self, locator="//h2")
        self.author = UIObject(parent=self, locator="//p[1]")


class MainPage(PageObject):
    """
    main page
    """
    PAGE_TITLE = "MainPage"
    PAGE_URL = "/index.html"

    def __init__(self) -> None:
        super().__init__()
        self.tile = Tile(parent=None, locator="//li")
        self.search_bar = UIObject(parent=None, locator="input[@id='searchBar']")

    @keyword
    def enter_search(self, search):
        """Enter to search bar"""
        self.browser.type_text(str(self.search_bar), search)

    def get_tile_count(self):
        return self.browser.get_element_count(str(self.tile))
