from . import DirectBase


class DirectChild(DirectBase):
    """Subclasses `DirectBase` via a zero-dot relative import (`from . import Foo`)."""
