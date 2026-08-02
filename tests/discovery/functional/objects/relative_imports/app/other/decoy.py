from BrowserPOM.uiobject import UIObject


class OtherBase(UIObject):
    """An unrelated UIObject subclass living in a sibling package, for output padding only."""

    decoy_marker = UIObject("css=.decoy")
