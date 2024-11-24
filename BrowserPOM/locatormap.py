# type: ignore
from __future__ import absolute_import, unicode_literals


class LocatorMap(dict):
    """LocatorMap - a dict-like object that supports dot notation

    This is used to map self._locators to a self.locator attribute,
    to make dealing with locators a bit more pleasant.
    """

    def __init__(self, args):
        super().__init__()  # Call to the parent class' __init__ if applicable

        if isinstance(args, dict):
            for key, value in args.items():
                # Validate key
                if " " in key or "." in key:
                    raise KeyError("Keys cannot have spaces or periods in them")

                # Assign value or recursively instantiate LocatorMap
                if not isinstance(value, dict):
                    self[key] = value
                else:
                    self.__setattr__(key, LocatorMap(value))

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super().__delitem__(key)
        del self.__dict__[key]
