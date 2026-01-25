"""Browser Page Object Model (POM) UIObject class."""

import contextlib
from urllib.parse import urlparse

import robot.api.logger
from Browser import Browser
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError


class PageObject:
    """Base class for page objects

    Classes that inherit from this class need to define the
    following class variables:

    PAGE_TITLE   the title of the page; used by the default
                 implementation of _is_current_page
    PAGE_URL     this should be the URL of the page, minus
                 the hostname and port (eg: /loginpage.html)
    """

    PAGE_URL: str = ""
    PAGE_TITLE: str = ""

    def __init__(self) -> None:
        """Initialize the page object."""
        self.logger = robot.api.logger
        with contextlib.suppress(RobotNotRunningError):
            BuiltIn().set_suite_variable(f"${self.__class__.__name__}", self)

    def run(self, eval_str: str) -> object:
        """Run a string as a Python expression in the context of this page object."""
        return eval(f"self.{eval_str}")

    @property
    def browser(self) -> Browser:
        """Returns the browser instance from robotframework-browser library
        Browser library has to be imported in robot file to reference
        """
        return BuiltIn().get_library_instance("BrowserPOM")

    def __str__(self) -> str:
        """Return a string representation of the page object."""
        return self.__class__.__name__

    def get_page_name(self) -> str:
        """Return the name of the current page"""
        return self.__class__.__name__

    def _is_current_page(self) -> bool:
        """Determine if this page object represents the current page.

        This works by comparing the current page title to the class
        variable PAGE_TITLE.

        Unless their page titles are unique, page objects should
        override this function. For example, a common solution is to
        look at the url of the current page, or to look for a specific
        heading or element on the page.

        """
        actual_title = self.browser.get_title()
        expected_title = self.PAGE_TITLE

        if actual_title.lower() == expected_title.lower():
            return True

        self.logger.info(f"expected title: '{expected_title}'")
        self.logger.info(f"  actual title: '{actual_title}'")
        return False

    @keyword
    def go_to_page(self, page_root: str | None = None) -> None:
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
        url = page_root if page_root is not None else self.browser.get_url()
        (scheme, netloc, _, _, _, _) = urlparse(url)
        url = f"{scheme}://{netloc}{self.PAGE_URL}"

        self.browser.go_to(url)
