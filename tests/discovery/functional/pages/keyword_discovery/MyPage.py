from BrowserPOM.pageobject import PageObject
from robot.api.deco import keyword


class MyPage(PageObject):
    PAGE_URL = "/"

    @keyword
    def enter_value(self, value: str, timeout: int = 10):
        """@keyword names are rendered in Robot Title Case, with parameter names shown in order."""

    @keyword
    def get_title(self) -> str:
        """A non-None return type annotation is shown after the parameter list."""
        return ""

    @keyword
    def do_action_annotated_none(self) -> None:
        """An explicit `-> None` return annotation is not shown."""

    @keyword
    def do_action_unannotated(self):
        """A missing return annotation is treated the same as `-> None` — not shown."""

    @property
    def _private_property_that_should_be_excluded(self) -> str:
        """Private properties are excluded from pages output, same as everywhere else."""
        return ""

    def helper_method_that_should_be_excluded(self):
        """Only @keyword-decorated methods are shown; plain methods are excluded."""
