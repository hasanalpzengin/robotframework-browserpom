from BrowserPOM.uiobject import UIObject


class SearchBar(UIObject):
        def __init__(self, locator: str, parent: UIObject | None = None):
                super().__init__(locator, parent=parent)

        def search(self, text: str):
                """Search for the given text in the search bar."""
                self.browser.type_text(str(self), text)