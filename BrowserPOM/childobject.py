from typing import get_type_hints, Type

from BrowserPOM.uiobject import UIObject


class ChildObject:
    def __init__(self, locator: str, is_list: bool = False) -> None:
        self.object_class: Type[UIObject] | None = None
        self.locator = locator
        self.is_list = is_list

    def __get__(self, obj, objtype=None):
        if not self.object_class:
            raise ValueError("Object class not known - did you forget to use type annotations?")
        parent = obj if isinstance(obj, UIObject) else None
        return self.object_class(parent=parent, locator=self.locator, is_list=self.is_list)

    def __set_name__(self, owner, name) -> None:
        self.object_class = get_type_hints(owner)[name]
        self.name = name
