"""PageObject for browser-backed UIObject iteration checks."""

from BrowserPOM import PageObject, UIObject


class Row(UIObject):
    """A row exposing a nested UIObject and a label property."""

    def __init__(self, locator: str, parent: UIObject | None = None) -> None:
        """Initialize the row's label under its indexed locator."""
        super().__init__(locator, parent)
        self.label_object = UIObject(".label", parent=self)

    @property
    def label(self) -> str:
        """Read the label through a property on the concrete subclass."""
        return self.browser.get_text(str(self.label_object))


class IterationPage(PageObject):
    """Expose both scoped and empty collections."""

    rows = Row(".row", parent=UIObject("#target"))
    missing = Row(".missing", parent=UIObject("#target"))

    def read_labels_in_python(self) -> list[str]:
        """Iterate in Python using the real Robot-managed Browser connection."""
        return [row.label for row in self.rows]
