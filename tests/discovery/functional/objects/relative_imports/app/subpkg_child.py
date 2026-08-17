from .subpkg import SubBase


class SubpkgChild(SubBase):
    """Subclasses `SubBase` via a one-dot relative import (`from .subpkg import Foo`)."""
