from BrowserPOM.uiobject import UIObject


class SharedBase(UIObject):
    """The real base class, reached from `app.component.deep` via a two-dot relative import."""

    marker = UIObject("css=.shared-marker")
