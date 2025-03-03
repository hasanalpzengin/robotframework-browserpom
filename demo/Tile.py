from BrowserPOM.childobject import ChildObject
from BrowserPOM.uiobject import UIObject


class Tile(UIObject):
    price: UIObject = ChildObject("//p[contains(@id, '_price')]")
    title: UIObject = ChildObject("//h2[contains(@id, '_title')]")
    author: UIObject = ChildObject("//p[contains(@id, '_author')]")