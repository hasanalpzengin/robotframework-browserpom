from BaseComponent import BaseComponent
from BrowserPOM.uiobject import UIObject


class Leaf(BaseComponent):
    """A UIObject subclass referenced from another file, to be resolved cross-file.

    Inherits from a custom intermediate base class (not directly from UIObject) —
    discovery must still recognize it as a UIObject subclass transitively.
    """

    # Class-level attribute using the positional locator argument form.
    label = UIObject("css=.label")
