from BrowserPOM.uiobject import UIObject


class Section(UIObject):
    @property
    def label(self) -> str:
        """@property members on nested UIObject children are excluded from `pages` output."""
        return ""
