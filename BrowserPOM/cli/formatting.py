"""Text rendering for `browserpom discover` output."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from BrowserPOM.cli.scanner import ChildUIObject, PageObjectClass, UIObjectClass


def _rel_path(project_root: Path, file_path: Path) -> str:
    try:
        return str(file_path.relative_to(project_root))
    except ValueError:
        return str(file_path)


def _format_child(child: "ChildUIObject", indent: int = 2) -> str:
    spacer = " " * indent
    locator_str = f'"{child.locator}"' if child.locator else ""
    lines = [f"{spacer}{child.name}: {child.type_name}({locator_str})"]
    lines.extend(_format_child(grandchild, indent + 2) for grandchild in child.children)
    return "\n".join(lines)


def _format_child_pages(child: "ChildUIObject", indent: int = 2) -> str:
    """Format a UIObject child for the pages command (no locators, no properties)."""
    spacer = " " * indent
    lines = [f"{spacer}{child.name}: {child.type_name}"]
    lines.extend(_format_child_pages(grandchild, indent + 2) for grandchild in child.children)
    return "\n".join(lines)


def _format_section(lines: list[str], name: str, indent: int, items: list[str]) -> None:
    """Append a section to `lines`: a header + indented items, or `Name: None` when empty."""
    prefix = " " * indent
    if items:
        lines.append(f"{prefix}{name}:")
        lines.extend(items)
    else:
        lines.append(f"{prefix}{name}: None")


def format_pageobject(cls: "PageObjectClass", project_root: Path) -> str:
    """Format a PageObjectClass for the pages command output."""
    lines: list[str] = [f"{cls.name}: {_rel_path(project_root, cls.file_path)}"]
    if cls.page_url is not None:
        lines.append(f"  PAGE_URL: {cls.page_url}")

    _format_section(
        lines,
        "Children",
        indent=2,
        items=[_format_child_pages(child, indent=4) for child in cls.children],
    )
    _format_section(
        lines,
        "Properties",
        indent=2,
        items=[f"    {prop.name}" for prop in cls.properties],
    )

    keyword_lines = []
    for kw in cls.keywords:
        params = ", ".join(kw.params)
        suffix = f" -> {kw.return_type}" if kw.return_type else ""
        keyword_lines.append(f"    {kw.robot_name}({params}){suffix}")
    _format_section(lines, "Keywords", indent=2, items=keyword_lines)

    return "\n".join(lines)


def format_uiobject(cls: "UIObjectClass", project_root: Path) -> str:
    """Format a UIObjectClass for the objects command output."""
    lines: list[str] = [f"{cls.name}: {_rel_path(project_root, cls.file_path)}"]

    _format_section(
        lines,
        "Children",
        indent=2,
        items=[_format_child(child, indent=4) for child in cls.children],
    )
    _format_section(
        lines,
        "Properties",
        indent=2,
        items=[f"    {prop.name}" for prop in cls.properties],
    )

    method_lines = []
    for method in cls.methods:
        params = ", ".join(method.params)
        method_lines.append(f"    {method.name}({params})")
    _format_section(lines, "Methods", indent=2, items=method_lines)

    return "\n".join(lines)
