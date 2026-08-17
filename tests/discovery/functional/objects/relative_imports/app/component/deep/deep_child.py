from ..shared.base import SharedBase


class DeepChild(SharedBase):
    """Subclasses `SharedBase` via a two-dot relative import (`from ..pkg.mod import Foo`).

    Also assigns a `SharedBase`-typed child, exercising `_resolve_type` for the same
    relative import — the exact fully-qualified match must win over the same-named
    decoy class in `app.other.decoy`.
    """

    shared_child = SharedBase("css=.deep-shared-child")
