from BrowserPOM.uiobject import UIObject


class Twig(UIObject):
    """A second, independently-typed child assigned in __init__ alongside Leaf."""

    tip = UIObject("css=.tip")
