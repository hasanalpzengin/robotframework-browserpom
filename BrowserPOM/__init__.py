"""Browser Page Object Model (POM) UIObject class."""

import contextlib
from pathlib import Path

from Browser import Browser
from Browser.utils import ScreenshotFileTypes, ScreenshotReturnType
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError

from .pageobject import PageObject
from .uiobject import UIObject


class BrowserPOM(Browser):
    """*PageObjectLibrary* is a lightweight library which supports using
    the page object pattern with
    [https://robotframework-browser.org/|BrowserLibrary].
    This library does not replace BrowserLibrary; rather, it
    provides a framework around which to use BrowserLibrary and the
    lower-level [http://selenium-python.readthedocs.org/|Python
    bindings to Playwright]

    This library provides the following keywords:

    | =Keyword Name=             | =Synopsis= |
    | Go to page                 | Goes to the given page in the browser |
    | The current page should be | Assert that the given page is displayed in the browser |

    PageObjectLibrary provides a PageObject class which should be used
    as the base class for other page objects. By inheriting from this
    class your keywords have access to the following pre-defined
    attributes and methods:

    | =Attribute/method=  | =Description=                             |
    | ``self.browser`` | A reference to the BrowserLibrary Reference  |
    | ``self.locator`` | A wrapper around the ``_locators`` dictionary        |
    | ``self.logger``  | A reference to the ``robot.api.logger`` instance     |

    = Using BrowserLibrary Keywords =

    Within your keywords you have access to the full power of
    BrowserLibrary. You can use ``self.browser`` to access the
    library keywords. The following example shows how to call the
    ``Capture Page Screenshot`` keyword:

    | self.browser.take_screenshot()

    = Creating Page Object Classes =

    Page objects should inherit from PageObjectLibrary.PageObject. At a minimum,
    the class should define the following attributes:

    | =Attribute= | =Description= |
    | ``PAGE_URL`` | The path to the current page, without the \
        hostname and port (eg: ``/dashboard.html``) |
    | ``PAGE_TITLE`` | The web page title. This is used by the \
        default implementation of ``_is_current_page``. |

    When using the keywords `Go To Page` or `The Current Page Should Be`, the
    PageObjectLibrary will call the method ``_is_current_page`` of the given page.
    By default this will compare the current page title to the ``PAGE_TITLE`` attribute
    of the page. If you are working on a site where the page titles are not unique,
    you can override this method to do any type of logic you need.

    = Page Objects are Normal Robot Libraries =

    All rules that apply to keyword libraries applies to page objects. For
    example, the libraries must be on ``PYTHONPATH``. You may also want to define
    ``ROBOT_LIBRARY_SCOPE``. Also, the filename and the classname must be identical (minus
    the ``.py`` suffix on the file).

    = Locators =

    When writing multiple keywords for a page, you often use the same locators in
    many places. PageObject allows you to define your locators in a dictionary,
    but them use them with a more convenient dot notation.

    To define locators, create a dictionary named ``_locators``. You can then access
    the locators via dot notation within your keywords as ``self.locator.<name>``. The
    ``_locators`` dictionary may have nested dictionaries.

    = Waiting for a Page to be Ready =

    One difficulty with writing Selenium tests is knowing when a page has refreshed.
    PageObject provides a context manager named ``_wait_for_page_refresh()`` which can
    be used to wrap a command that should result in a page refresh. It will get a
    reference to the DOM, run the body of the context manager, and then wait for the
    DOM to change before returning.

    = Example Page Object Definition =

    | from PageObjectLibrary import PageObject
    | from robot.libraries.BuiltIn import BuiltIn
    |
    | class LoginPage(PageObject):
    |     PAGE_TITLE = "Login - PageObjectLibrary Demo"
    |     PAGE_URL = "/"
    |
    |    _locators = {
    |        "username": "id=id_username",
    |        "password": "id=id_password",
    |        "submit_button": "id=id_submit",
    |    }
    |
    |    @keyword
    |    def enter_search(self, search):
    |       self.browser.type_text(self.locator.search_bar, search)
    |
    """

    ROBOT_LIBRARY_SCOPE = "TEST SUITE"

    def __init__(self) -> None:
        """Initialize the BrowserPOM library."""
        addon_path = Path(__file__).parent / "addons" / "playwright_page_method.js"
        with contextlib.suppress(RobotNotRunningError):
            BuiltIn().set_library_search_order("BrowserPOM", "Browser")
        super().__init__(jsextension=str(addon_path))

    @keyword
    def take_screenshot(self, *args, **kwargs):  # noqa:ANN002,ANN003,ANN201
        """Take a screenshot, and additionally attach it to the Allure report if
        the Allure listener is installed.
        """
        path = self._browser_control.take_screenshot(*args, **kwargs)
        try:
            import allure  # noqa:PLC0415

            allure.attach.file(
                path,
                name="screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
        except ImportError:
            pass
        return path
