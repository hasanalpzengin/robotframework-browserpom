"""Browser Page Object Model (POM) UIObject class."""
from urllib.parse import urlparse

import robot
from robot.libraries.BuiltIn import BuiltIn

from BrowserPOM.pageobject import PageObject


class BrowserPomKeywords:
    """BrowserPOM Library's generic keywords

    | =Keyword Name=             |
    | Go to page                 |
    | The current page should be |
    """

    ROBOT_LIBRARY_SCOPE = "TEST SUITE"

    def __init__(self) -> None:
        """Initialize the BrowserPOM keywords library."""
        self.builtin = BuiltIn()
        self.logger = robot.api.logger

    def go_to_page(self, page_name: str, page_root: str | None = None) -> None:
        """Go to the url for the given page object.

        Unless explicitly provided, the URL root will be based on the
        root of the current page. For example, if the current page is
        http://www.example.com:8080 and the page object URL is
        ``/login``, the url will be http://www.example.com:8080/login

        == Example ==

        Given a page object named ``ExampleLoginPage`` with the URL
        ``/login``, and a browser open to ``http://www.example.com``, the
        following statement will go to ``http://www.example.com/login``,
        and place ``ExampleLoginPage`` at the front of Robot's library
        search order.

        | Go to Page    ExampleLoginPage

        The effect is the same as if you had called the following three
        keywords:

        | SeleniumLibrary.Go To       http://www.example.com/login
        | Import Library              ExampleLoginPage
        | Set Library Search Order    ExampleLoginPage

        Tags: selenium, page-object

        """
        page = self._get_page_object(page_name)

        url = page_root if page_root is not None else page.browser.get_url()
        (scheme, netloc, _, _, _, _) = urlparse(url)
        url = f"{scheme}://{netloc}{page.PAGE_URL}"

        page.browser.go_to(url)

    def _get_page_object(self, page_name: str) -> PageObject:
        """Import the page object if necessary, then return the handle to the library

        Note: If the page object has already been imported, it won't be imported again.
        """
        try:
            page = self.builtin.get_library_instance(page_name)
        except RuntimeError:
            self.builtin.import_library(page_name)
            page = self.builtin.get_library_instance(page_name)

        return page
