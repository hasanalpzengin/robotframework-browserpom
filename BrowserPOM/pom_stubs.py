"""Helper script that can be passed as variable file to robotcode LSP.
It creates placeholders for the PageObjects, so that robotcode does not
complain about unknown variables.
"""

import ast
from pathlib import Path


def get_variables(base_path: str) -> dict[str, str]:
    """Return a mapping of class-name -> dummy for classes that inherit PageObject.

    Scans Python modules under ``base_path`` and parses their AST. Only classes
    whose base(s) directly reference `PageObject` (either as a Name or an
    Attribute) are included.
    """

    def _inherits_pageobject(cls_node: ast.ClassDef) -> bool:
        """Return True if the class AST node inherits from PageObject.

        We look for bases that are ast.Name, ast.Attribute, ast.Subscript,
        or ast.Call wrapping 'PageObject'.
        """

        def _is_pageobject_node(node: ast.AST | None) -> bool:
            """Recursively check if a node or its relevant child refers
            to 'PageObject'.
            """
            if node is None:
                return False

            # case PageObject
            if isinstance(node, ast.Name):
                return node.id == "PageObject"

            # case some_module.PageObject
            if isinstance(node, ast.Attribute):
                return getattr(node, "attr", None) == "PageObject"

            # case PageObject[T]
            if isinstance(node, ast.Subscript):
                return _is_pageobject_node(getattr(node, "value", None))

            # case PageObject(metaclass=...)
            if isinstance(node, ast.Call):
                return _is_pageobject_node(getattr(node, "func", None))

            return False

        # Return True if any base class matches
        return any(_is_pageobject_node(base) for base in cls_node.bases)

    variables = {}
    modules = Path(base_path).rglob("*.py")
    for module in modules:
        try:
            tree = ast.parse(module.read_text("utf8"))
            variables.update(
                {node.name: node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef) and _inherits_pageobject(node)},
            )
        except Exception:  # noqa: S112,BLE001
            # ignore parse errors or unreadable files
            continue

    return variables
