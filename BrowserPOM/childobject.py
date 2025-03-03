from typing import Type, get_type_hints

from BrowserPOM.uiobject import UIObject


class ChildObject:
    """
    Represents a child object in the Browser Page Object Model (POM).

    Attributes:
        object_class (Type[UIObject] | None): The class type of the UI object. Initially set to None.
        locator (str): The locator string used to identify the UI object.
    """

    def __init__(self, locator: str) -> None:
        """
        Initializes a ChildObject instance.

        Args:
            locator (str): The locator string used to identify the UI object.
        """
        self.object_class: Type[UIObject] | None = None
        self.locator = locator

    def __get__(self, obj, objtype=None):
        """
        Retrieves the UI object instance.

        Args:
            obj: The parent object, expected to be an instance of UIObject.
            objtype: The type of the parent object. Default is None.

        Returns:
            UIObject: An instance of the UI object class.

        Raises:
            ValueError: If the object class is not known, indicating that type annotations might be missing.
        """
        if not self.object_class:
            raise ValueError("Object class not known - did you forget to use type annotations?")
        parent = obj if isinstance(obj, UIObject) else None
        return self.object_class(parent=parent, locator=self.locator)

    def __set_name__(self, owner, name) -> None:
        """
        Sets the name of the child object and determines its class type.

        Args:
            owner: The owner class that contains the child object.
            name (str): The name of the child object.
        """
        self.object_class = get_type_hints(owner)[name]
