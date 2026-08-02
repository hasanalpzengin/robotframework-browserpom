from BrowserPOM.pageobject import PageObject
from BrowserPOM.uiobject import UIObject
from Section import Section


class MyPage(PageObject):
    PAGE_URL = "/"

    # A class-level attribute whose type is a named UIObject subclass — the
    # hierarchy line must show "Section", not the generic "UIObject".
    section = Section("css=.section")

    # A class-level attribute of the literal base UIObject type, directly on
    # the page (as opposed to `section`, which is class-level but named, and
    # `body` below, which is base-typed but __init__-assigned).
    status = UIObject("css=.status")

    def __init__(self):
        super().__init__()
        # An __init__-assigned child of the base UIObject type must also
        # appear in the hierarchy, alongside class-level attributes.
        self.body = UIObject("css=.body")
