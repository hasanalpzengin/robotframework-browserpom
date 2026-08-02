from BrowserPOM.pageobject import PageObject
from Section import Section


class MyPage(PageObject):
    """No PAGE_URL is defined here — the PAGE_URL line must be absent from output."""

    section = Section("css=.section")

    @property
    def title(self) -> str:
        """A direct @property on the PageObject itself is shown."""
        return ""
