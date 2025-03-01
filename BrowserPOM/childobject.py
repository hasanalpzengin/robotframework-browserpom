from typing import Type, get_type_hints

from BrowserPOM.uiobject import UIObject


class ChildObject:
    def __init__(self, locator: str) -> None:
        self.object_class: Type[UIObject] | None = None
        self.locator = locator

    def __get__(self, obj, objtype=None):
        if not self.object_class:
            raise ValueError("Object class not known - did you forget to use type annotations?")
        parent = obj if isinstance(obj, UIObject) else None
        return self.object_class(parent=parent, locator=self.locator)

    def __set_name__(self, owner, name) -> None:
        self.object_class = get_type_hints(owner)[name]
