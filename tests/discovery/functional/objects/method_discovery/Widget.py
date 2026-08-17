from BrowserPOM.uiobject import UIObject
from robot.api.deco import keyword


def retry(times):
    """A generic parameterized decorator, unrelated to Robot Framework."""

    def decorator(f):
        return f

    return decorator


def log_action(f):
    """An uncalled decorator, applied directly (not via a factory call like @retry(3))."""
    return f


class Widget(UIObject):
    def click_that_should_be_included(self, times=1):
        """A directly-defined, non-private, non-@keyword method is shown with its parameter signature."""

    def click_that_should_show_params_in_declared_order(self, a, b, c, /, d):
        """Positional-only parameters (before `/`) must be listed in declaration order."""

    def _private_method_that_should_be_excluded(self):
        """Methods whose name starts with an underscore are excluded."""

    @keyword
    def keyword_decorated_method_that_should_be_excluded(self):
        """@keyword-decorated methods belong to the `pages` output, not `objects` — excluded here."""

    @retry(3)
    def other_decorator_method_that_should_be_included(self):
        """Decorators other than @keyword must not influence method discovery — still included."""

    @log_action
    def uncalled_decorator_method_that_should_be_included(self):
        """An uncalled decorator (a bare Name node, not a Call node) must also not suppress discovery."""

    def submit_that_should_show_keyword_only_param(
        self,
        value: str,
        *,
        timeout: int = 10,
    ):
        """Keyword-only parameters (after `*`) are included in the parameter signature."""
