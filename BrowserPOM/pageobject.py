from __future__ import absolute_import, unicode_literals

from abc import ABCMeta

import robot.api
from Browser import Browser
from robot.libraries.BuiltIn import BuiltIn

from .locatormap import LocatorMap  # type: ignore[attr-defined]


class PageObject(metaclass=ABCMeta):
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

    def __init__(self):
        self.logger = robot.api.logger
        self.locator = LocatorMap(getattr(self, "_locators", {}))
        self.builtin = BuiltIn()
        self.builtin.set_local_variable(f"${self.__class__.__name__}", self.locator)

    @property
    def browser(self) -> Browser:
        """
        Returns the browser instance from robotframework-browser library
        Browser library has to be imported in robot file to reference
        """
        return self.builtin.get_library_instance("Browser")

    def __str__(self):
        return self.__class__.__name__

    def get_page_name(self):
        """Return the name of the current page"""
        return self.__class__.__name__

    def _is_current_page(self):
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