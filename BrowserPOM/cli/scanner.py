"""AST-based discovery of UIObject subclasses."""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path  # noqa: TC003
from typing import TYPE_CHECKING

from BrowserPOM.cli.exceptions import DiscoveryError

if TYPE_CHECKING:
    from collections.abc import Iterator, Sequence


@dataclass
class MethodInfo:
    """A directly-defined method on a UIObject subclass."""

    name: str
    params: list[str]


@dataclass
class PropertyInfo:
    """A directly-defined @property on a UIObject subclass."""

    name: str


@dataclass
class ChildUIObject:
    """A child UIObject attribute with its locator and resolved children."""

    name: str
    type_name: str
    locator: str | None
    children: list[ChildUIObject] = field(default_factory=list)
    properties: list[PropertyInfo] = field(default_factory=list)


@dataclass
class KeywordInfo:
    """A @keyword method on a PageObject."""

    name: str
    robot_name: str
    params: list[str]
    return_type: str | None


@dataclass
class PageObjectClass:
    """Discovered information about a PageObject subclass."""

    name: str
    module_path: str
    file_path: Path
    page_url: str | None = None
    children: list[ChildUIObject] = field(default_factory=list)
    properties: list[PropertyInfo] = field(default_factory=list)
    keywords: list[KeywordInfo] = field(default_factory=list)


@dataclass
class UIObjectClass:
    """Discovered information about a UIObject subclass."""

    name: str
    module_path: str
    file_path: Path
    children: list[ChildUIObject] = field(default_factory=list)
    properties: list[PropertyInfo] = field(default_factory=list)
    methods: list[MethodInfo] = field(default_factory=list)


class _ModuleImports:
    """Tracks import mappings for a single module."""

    def __init__(self) -> None:
        # local_name -> (module_path, imported_name)
        self._mappings: dict[str, tuple[str, str]] = {}

    def add(self, local_name: str, module_path: str, imported_name: str) -> None:
        self._mappings[local_name] = (module_path, imported_name)

    def resolve(self, local_name: str) -> tuple[str | None, str]:
        """Return (module_path, imported_name) for a local name, or (None, local_name)."""
        if local_name in self._mappings:
            return self._mappings[local_name]
        return (None, local_name)


@dataclass
class _RawClass:
    """Raw parsed information about a class, before UIObject filtering."""

    name: str
    module_name: str
    file_path: Path
    bases: list[str]
    body: list[ast.stmt]
    init_body: list[ast.stmt]
    imports: _ModuleImports

    @property
    def full_name(self) -> str:
        """The fully-qualified `module.ClassName` name used as a registry/index key."""
        return f"{self.module_name}.{self.name}"


def _extract_locator(call: ast.Call) -> str | None:
    """Extract the locator string from a UIObject constructor call.

    Checks the first positional string argument, then a keyword argument
    named ``locator``.
    """
    for arg in call.args:
        if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
            return arg.value
    for kw in call.keywords:
        if kw.arg == "locator" and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
            return kw.value.value
    return None


def _has_decorator(func: ast.FunctionDef | ast.AsyncFunctionDef, name: str) -> bool:
    for dec in func.decorator_list:
        # bare:      @keyword
        if isinstance(dec, ast.Name) and dec.id == name:
            return True
        # dotted:    @deco.keyword
        if isinstance(dec, ast.Attribute) and dec.attr == name:
            return True
        # called:    @keyword("Custom Name")  or  @deco.keyword(...)
        if isinstance(dec, ast.Call):
            inner = dec.func
            if isinstance(inner, ast.Name) and inner.id == name:
                return True
            if isinstance(inner, ast.Attribute) and inner.attr == name:
                return True
    return False


def _is_property(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    return _has_decorator(func, "property")


def _is_keyword(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    return _has_decorator(func, "keyword")


def _method_params(func: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
    """Return parameter names excluding self/cls."""
    params = [arg.arg for arg in func.args.posonlyargs if arg.arg not in {"self", "cls"}]
    params.extend(arg.arg for arg in func.args.args if arg.arg not in {"self", "cls"})
    params.extend(arg.arg for arg in func.args.kwonlyargs)
    if func.args.vararg:
        params.append(f"*{func.args.vararg.arg}")
    if func.args.kwarg:
        params.append(f"**{func.args.kwarg.arg}")
    return params


def _is_private(name: str) -> bool:
    return name.startswith("_")


def _is_dunder(name: str) -> bool:
    return name.startswith("__") and name.endswith("__")


def _class_name(node: ast.expr) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parts = []
        current: ast.expr = node
        while isinstance(current, ast.Attribute):
            parts.append(current.attr)
            current = current.value
        if isinstance(current, ast.Name):
            parts.append(current.id)
        return ".".join(reversed(parts))
    return None


def _build_module_name(file_path: Path, root: Path) -> str:
    """Build a dotted module name from a file path relative to a root."""
    try:
        rel = file_path.relative_to(root)
    except ValueError:
        rel = file_path
    parts = list(rel.with_suffix("").parts)
    # Strip leading empty part from absolute-path fallback
    if parts and parts[0] == "/":
        parts = parts[1:]
    # `__init__.py` modules are addressed by their package name, not
    # `<package>.__init__` — strip the trailing component so relative-import
    # resolution (which reasons about a module's *package*) lines up with
    # how classes defined in `__init__.py` are keyed.
    if parts and parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def _package_name(module_name: str, file_path: Path) -> str:
    """Return the dotted package name that `module_name` belongs to.

    For a package's `__init__.py`, the module *is* the package. For any
    other module, the package is everything but the last component.
    """
    if not module_name:
        return ""
    if file_path.name == "__init__.py":
        return module_name
    if "." in module_name:
        return module_name.rsplit(".", 1)[0]
    return ""


def _resolve_relative_module(module: str, level: int, package: str) -> str:
    """Resolve a relative import's absolute module path (mirrors importlib._bootstrap._resolve_name)."""
    bits = package.rsplit(".", level - 1)
    base = bits[0] if bits else ""
    if module:
        return f"{base}.{module}" if base else module
    return base


def _child_from_call(name: str, call: ast.Call) -> ChildUIObject | None:
    """Build a ChildUIObject from an attribute name and a constructor Call node.

    Returns ``None`` when the callable cannot be resolved to a name.
    """
    type_name = _class_name(call.func)
    if type_name is None:
        return None
    return ChildUIObject(name=name, type_name=type_name, locator=_extract_locator(call))


def _extract_class_level_children(body: list[ast.stmt]) -> list[ChildUIObject]:
    """Extract children from class-level `name = SomeType(...)` assignments."""
    children: list[ChildUIObject] = []
    for item in body:
        if not isinstance(item, ast.Assign) or not isinstance(item.value, ast.Call):
            continue
        for target in item.targets:
            if isinstance(target, ast.Name) and not _is_private(target.id):
                child = _child_from_call(target.id, item.value)
                if child is not None:
                    children.append(child)
    return children


def _extract_init_children(init_body: list[ast.stmt]) -> list[ChildUIObject]:
    """Extract children from `self.name = SomeType(...)` assignments in `__init__`."""
    children: list[ChildUIObject] = []
    for stmt in init_body:
        if not isinstance(stmt, ast.Assign) or not isinstance(stmt.value, ast.Call):
            continue
        for target in stmt.targets:
            if (
                isinstance(target, ast.Attribute)
                and isinstance(target.value, ast.Name)
                and target.value.id == "self"
                and not _is_private(target.attr)
            ):
                child = _child_from_call(target.attr, stmt.value)
                if child is not None:
                    children.append(child)
    return children


def _extract_properties(body: list[ast.stmt]) -> list[PropertyInfo]:
    """Extract `@property` members from a class body, excluding private/dunder names."""
    return [
        PropertyInfo(name=item.name)
        for item in body
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
        and _is_property(item)
        and not _is_private(item.name)
        and not _is_dunder(item.name)
    ]


def _resolve_base_name(base_name: str, imports: _ModuleImports) -> str:
    """Resolve a local base class name to its fully qualified name."""
    mod, name = imports.resolve(base_name)
    if mod:
        return f"{mod}.{name}"
    return name


def _parse_module(file_path: Path, root: Path) -> list[_RawClass] | None:  # noqa: C901
    """Parse a single Python file and return raw class definitions."""
    module_name = _build_module_name(file_path, root)
    package_name = _package_name(module_name, file_path)
    imports = _ModuleImports()

    try:
        source = file_path.read_text(encoding="utf-8")
    except OSError:
        return None

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                local = alias.asname or alias.name
                imports.add(local, alias.name, alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if node.level:
                module = _resolve_relative_module(module, node.level, package_name)
            for alias in node.names:
                local = alias.asname or alias.name
                imports.add(local, module, alias.name)

    raw_classes: list[_RawClass] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            bases = [bname for base in node.bases if (bname := _class_name(base)) is not None]

            init_body: list[ast.stmt] = []
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name == "__init__":
                    init_body = item.body

            raw_classes.append(
                _RawClass(
                    name=node.name,
                    module_name=module_name,
                    file_path=file_path,
                    bases=bases,
                    body=node.body,
                    init_body=init_body,
                    imports=imports,
                ),
            )

    return raw_classes


def _to_robot_title_case(name: str) -> str:
    """Convert a Python snake_case name to Robot Framework Title Case."""
    return " ".join(word.capitalize() for word in name.split("_"))


def _extract_return_type(func: ast.FunctionDef | ast.AsyncFunctionDef) -> str | None:
    """Extract the return type annotation as a string, or None if absent or None-typed."""
    if func.returns is None:
        return None
    unparsed = ast.unparse(func.returns)
    if unparsed in {"None", "type[None]"}:
        return None
    return unparsed


def _extract_page_url(body: list[ast.stmt]) -> str | None:
    """Extract the PAGE_URL string constant from a class body, if present."""
    for item in body:
        if isinstance(item, ast.Assign):
            for target in item.targets:
                if (
                    isinstance(target, ast.Name)
                    and target.id == "PAGE_URL"
                    and isinstance(item.value, ast.Constant)
                    and isinstance(item.value.value, str)
                ):
                    return item.value.value
        elif (
            isinstance(item, ast.AnnAssign)
            and isinstance(item.target, ast.Name)
            and item.target.id == "PAGE_URL"
            and item.value is not None
            and isinstance(item.value, ast.Constant)
            and isinstance(item.value.value, str)
        ):
            return item.value.value
    return None


class Scanner:
    """Scans configured paths for UIObject subclasses."""

    def __init__(self, project_root: Path, paths: Sequence[str]) -> None:
        """Initialize a new Scanner."""
        self.project_root = project_root
        self.paths = list(paths)
        self._raw_classes: list[_RawClass] = []
        self._raw_classes_by_full_name: dict[str, _RawClass] = {}
        self._raw_classes_by_name_and_file: dict[tuple[str, Path], _RawClass] = {}
        self._registry: dict[str, UIObjectClass] = {}

    def _collect_files(self) -> Iterator[Path]:
        for p in self.paths:
            target = self.project_root / p
            if not target.exists():
                raise DiscoveryError(
                    f"Configured scan target does not exist on disk: {p}",
                )
            if target.is_file() and target.suffix == ".py":
                yield target
            elif target.is_dir():
                yield from target.rglob("*.py")

    @staticmethod
    def _is_subclass_of(raw: _RawClass, base_name: str, resolved_set: set[str]) -> bool:
        """Return True if `raw` directly or transitively subclasses `base_name`.

        `resolved_set` holds the fully-qualified names of classes already
        confirmed to be subclasses of `base_name`, so this also picks up
        indirect (multi-level) inheritance as the set grows via fixed-point
        iteration.
        """
        for base in raw.bases:
            resolved = _resolve_base_name(base, raw.imports)
            if resolved == base_name or resolved.endswith(f".{base_name}"):
                return True
            if resolved in resolved_set:
                return True
            # Also check short name
            if resolved.split(".")[-1] == base_name:
                return True
        return False

    def _resolve_subclasses(self, base_name: str) -> set[str]:
        """Resolve the fully-qualified names of all classes subclassing `base_name`.

        Repeatedly walks `self._raw_classes_by_full_name`, propagating
        subclass membership until a fixed point is reached (so indirect
        subclasses are also found).
        """
        resolved_set: set[str] = set()
        changed = True
        while changed:
            changed = False
            for full_name, raw in self._raw_classes_by_full_name.items():
                if full_name in resolved_set:
                    continue
                if raw.name == base_name:
                    continue
                if self._is_subclass_of(raw, base_name, resolved_set):
                    resolved_set.add(full_name)
                    changed = True
        return resolved_set

    def _resolve_type(
        self,
        type_name: str,
        local_imports: _ModuleImports,
    ) -> UIObjectClass | None:
        """Resolve a type name to its UIObjectClass definition, if any."""
        mod, name = local_imports.resolve(type_name)
        full_name = f"{mod}.{name}" if mod else name
        # Try exact match
        if full_name in self._registry:
            return self._registry[full_name]
        # Try just the name if unique
        candidates = [cls for key, cls in self._registry.items() if key.endswith(f".{name}") or key == name]
        if len(candidates) == 1:
            return candidates[0]
        return None

    def _expand_children(
        self,
        children: list[ChildUIObject],
        local_imports: _ModuleImports,
    ) -> None:
        for child in children:
            resolved = self._resolve_type(child.type_name, local_imports)
            if resolved is not None:
                child.properties = list(resolved.properties)
                child.children = [
                    ChildUIObject(
                        name=c.name,
                        type_name=c.type_name,
                        locator=c.locator,
                        children=[],
                    )
                    for c in resolved.children
                ]
                self._expand_children(
                    child.children,
                    self._get_imports_for_class(resolved),
                )

    def _get_imports_for_class(self, cls: UIObjectClass) -> _ModuleImports:
        raw = self._raw_classes_by_name_and_file.get((cls.name, cls.file_path))
        if raw is not None:
            return raw.imports
        return _ModuleImports()

    def _build_indexes(self) -> None:
        """Build lookup indexes over `self._raw_classes`, once per scan."""
        self._raw_classes_by_full_name = {raw.full_name: raw for raw in self._raw_classes}
        self._raw_classes_by_name_and_file = {(raw.name, raw.file_path): raw for raw in self._raw_classes}

    @staticmethod
    def _extract_children_and_properties(raw: _RawClass) -> tuple[list[ChildUIObject], list[PropertyInfo]]:
        """Extract class-level and `__init__`-assigned children plus `@property` members.

        Shared between UIObject and PageObject extraction, which each layer
        their own extras (methods, or page_url/keywords) on top.
        """
        children = _extract_class_level_children(raw.body)
        properties = _extract_properties(raw.body)
        children.extend(_extract_init_children(raw.init_body))
        return children, properties

    @classmethod
    def _extract_class_info(cls, raw: _RawClass) -> UIObjectClass:
        children, properties = cls._extract_children_and_properties(raw)
        uiobject = UIObjectClass(
            name=raw.name,
            module_path=raw.module_name,
            file_path=raw.file_path,
            children=children,
            properties=properties,
        )

        for item in raw.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and (
                not _is_property(item) and not _is_keyword(item) and not _is_private(item.name) and not _is_dunder(item.name)
            ):
                uiobject.methods.append(
                    MethodInfo(name=item.name, params=_method_params(item)),
                )

        return uiobject

    @classmethod
    def _extract_page_info(cls, raw: _RawClass) -> PageObjectClass:
        children, properties = cls._extract_children_and_properties(raw)
        page = PageObjectClass(
            name=raw.name,
            module_path=raw.module_name,
            file_path=raw.file_path,
            page_url=_extract_page_url(raw.body),
            children=children,
            properties=properties,
        )

        for item in raw.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and (
                _is_keyword(item) and not _is_private(item.name) and not _is_dunder(item.name)
            ):
                page.keywords.append(
                    KeywordInfo(
                        name=item.name,
                        robot_name=_to_robot_title_case(item.name),
                        params=_method_params(item),
                        return_type=_extract_return_type(item),
                    ),
                )

        return page

    def scan_pages(self) -> list[PageObjectClass]:
        """Scan all configured targets and return PageObject subclasses alphabetically."""
        # Ensure UIObject registry is built first (needed for hierarchy expansion)
        if not self._raw_classes:
            self.scan()

        pageobject_set = self._resolve_subclasses("PageObject")

        pages: list[PageObjectClass] = []
        for full_name, raw in self._raw_classes_by_full_name.items():
            if full_name not in pageobject_set:
                continue
            page = self._extract_page_info(raw)
            self._expand_children(page.children, raw.imports)
            pages.append(page)

        pages.sort(key=lambda p: p.name)
        return pages

    def scan(self) -> list[UIObjectClass]:
        """Scan all configured targets and return UIObject subclasses alphabetically."""
        # First pass: collect raw classes from all files
        for file_path in self._collect_files():
            raw_list = _parse_module(file_path, self.project_root)
            if raw_list is None:
                continue
            self._raw_classes.extend(raw_list)

        # Build lookup indexes once, used throughout the remaining passes
        # instead of repeated O(n) linear scans over `self._raw_classes`.
        self._build_indexes()

        # Second pass: determine which classes are UIObject subclasses
        # Start with direct UIObject subclasses, then propagate
        uiobject_set = self._resolve_subclasses("UIObject")

        # Third pass: build registry from UIObject subclasses
        for full_name, raw in self._raw_classes_by_full_name.items():
            if full_name not in uiobject_set:
                continue
            cls = self._extract_class_info(raw)
            self._registry[full_name] = cls

        # Fourth pass: expand children recursively
        for full_name, raw in self._raw_classes_by_full_name.items():
            if full_name in self._registry:
                cls = self._registry[full_name]
                self._expand_children(cls.children, raw.imports)

        # Return flat alphabetical list
        result = list(self._registry.values())
        result.sort(key=lambda c: c.name)
        return result
