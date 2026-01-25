# ruff:noqa
from BrowserPOM import PageObject, UIObject


class ListItem(UIObject):
    def __init__(self, locator: str, parent: UIObject | None = None) -> None:
        super().__init__(locator, parent)


class POM(PageObject):
    # variant 1: uses single quotes inside xPath
    electronics = ListItem("//li[@data-category='electronics']")
    # variant 2: uses double quotes inside xPath
    books = ListItem('//li[@data-category="books"]')
