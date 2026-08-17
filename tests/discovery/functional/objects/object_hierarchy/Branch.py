from BrowserPOM.uiobject import UIObject
from Leaf import Leaf
from Twig import Twig


class Branch(UIObject):
    """Exercises cross-file resolution, __init__-assigned children, and >=2 levels of nesting."""

    # Class-level attribute using the keyword locator argument form.
    header = UIObject(locator="css=.header")

    def __init__(self, locator, parent=None):
        super().__init__(locator, parent=parent)
        # __init__-assigned child whose type (Leaf) is defined in another file and
        # must be resolved cross-file to expand its own children (label) —
        # giving a hierarchy at least two levels deep: leaf -> label.
        self.leaf = Leaf("css=.leaf", parent=self)
        # A second, independently-typed __init__-assigned child — must be
        # resolved and expanded on its own, alongside `leaf`.
        self.twig = Twig("css=.twig", parent=self)
