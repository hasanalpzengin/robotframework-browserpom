from BrowserPOM.uiobject import UIObject


class Section(UIObject):
    """A named UIObject subclass referenced from a PageObject."""

    # A nested child one level below `section` — the pages hierarchy must expand
    # recursively to reach it, and must never show its locator string.
    inner = UIObject("css=.inner")
