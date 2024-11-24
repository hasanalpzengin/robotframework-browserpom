from robot.api.deco import keyword

from BrowserPOM.pageobject import PageObject


class MainPage(PageObject):
    """
    main page
    """
    PAGE_TITLE = "MainPage"
    PAGE_URL = "/index.html"

    _locators = {
        "tile": {
            "skeleton": "//li",
            "price_label": "//li//p[2]",
            "title": "//li//h2",
            "author": "//li//p[1]"
        },
        "search_bar": "input[@id='searchBar']"
    }

    @keyword
    def enter_search(self, search):
        """Enter to search bar"""
        self.browser.type_text(self.locator.search_bar, search)

    def get_tile_count(self):
        return self.browser.get_element_count(self.locator.get("tile").get("skeleton"))
