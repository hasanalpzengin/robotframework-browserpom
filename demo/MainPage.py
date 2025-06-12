from robot.api.deco import keyword

from BrowserPOM.pageobject import PageObject
from BrowserPOM.uiobject import UIObject
from demo.Content import Content
from demo.SearchBar import SearchBar


class MainPage(PageObject):
    ROBOT_LIBRARY_SCOPE = "SUITE"
    """
    main page
    """
    PAGE_TITLE = "MainPage"
    PAGE_URL = "/index.html"

    content_area = Content(".ui-content")
    search_bar = SearchBar("//input[@id='searchBar']")

    @keyword
    def enter_search(self, search):
        """Enter to search bar"""
        self.browser.type_text(str(self.search_bar), search)

    def get_tile_count(self):
        return self.browser.get_element_count(str(self.content_area.tile))
