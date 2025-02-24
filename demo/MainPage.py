from robot.api.deco import keyword

from BrowserPOM.childobject import ChildObject
from BrowserPOM.pageobject import PageObject
from BrowserPOM.uiobject import UIObject


class Tile(UIObject):
    price_label: UIObject = ChildObject("//p[2]")
    title: UIObject = ChildObject("//h2")
    author: UIObject = ChildObject("//p[1]")


class MainPage(PageObject):
    """
    main page
    """
    PAGE_TITLE = "MainPage"
    PAGE_URL = "/index.html"

    tile: Tile = ChildObject("//li")
    search_bar: UIObject = ChildObject("input[@id='searchBar']")

    @keyword
    def enter_search(self, search):
        """Enter to search bar"""
        self.browser.type_text(str(self.search_bar), search)

    def get_tile_count(self):
        return self.browser.get_element_count(str(self.tile))
