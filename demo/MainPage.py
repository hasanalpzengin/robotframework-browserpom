"""Demo main page object."""

from BrowserPOM.decorator import on_error_trigger
from BrowserPOM.pageobject import PageObject
from BrowserPOM.uiobject import UIObject
from robot.api.deco import keyword

from demo.Content import Content
from demo.SearchBar import SearchBar


class MainPage(PageObject):
    """Page object for the demo main page."""

    ROBOT_LIBRARY_SCOPE = "SUITE"
    PAGE_TITLE = "MainPage"
    PAGE_URL = "/index.html"

    content_area = Content(".ui-content")
    search_bar = SearchBar("//input[@id='searchBar']")
    error_element = UIObject("//div[@id='error']")

    @keyword
    def enter_search(self, search: str) -> None:
        """Enter text into the search bar."""
        self.browser.type_text(str(self.search_bar), search)

    @keyword
    @on_error_trigger
    def fail_keyword(self) -> None:
        """Read the error element text to trigger wrapped error handling."""
        self.browser.get_text(str(self.error_element))

    def get_tile_count(self) -> int:
        """Return the number of tiles displayed in the content area."""
        return self.browser.get_element_count(str(self.content_area.tile))
