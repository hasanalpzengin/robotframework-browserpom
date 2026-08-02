from BrowserPOM.uiobject import UIObject


class Widget(UIObject):
    @property
    def title(self) -> str:
        """A direct, non-private, non-dunder @property is included."""
        return ""

    @property
    def _private_property_that_should_be_excluded(self) -> str:
        """Properties whose name starts with an underscore are excluded."""
        return ""

    @property
    def __dunder_property_that_should_be_excluded__(self) -> str:
        """Dunder-named properties are excluded."""
        return ""
