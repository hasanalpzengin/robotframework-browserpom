---
name: browserpom-create-pageobjects
description: Discover existing UIObjects and create or modify PageObject and UIObject classes for a robotframework-browserpom project.
---

# BrowserPOM — Create PageObjects and UIObjects

Use this skill when creating, modifying, or extending Python `PageObject` and `UIObject` classes in a `robotframework-browserpom` project.

## Discover Existing Objects

Before adding a new component, run discovery to avoid duplicating existing UIObjects:

```bash
browserpom discover objects
```

This requires a `[tool.browserpom.discover]` section in the project's `pyproject.toml`. If the section is missing the CLI prints a descriptive error — add the section and retry:

```toml
[tool.browserpom.discover]
paths = ["demo/"]
```

Run the command from the directory containing `pyproject.toml` and in the same Python environment as the tests.

### Interpret Object Output

Read output as blank-line-separated class blocks. Each block starts with `ClassName: path/to/file.py`.

- Child entries include locator expressions.
- Use the source path to resolve duplicate class names across packages.

Read the source file only if the compact output does not include required details.

### Reuse vs. Create

- Reuse a compatible local component instead of duplicating it.
- When modifying or extending behaviour, prefer local source objects.
- Use an installed-package object only when: the installed version matches the version declared in the project's dependencies, the public API (method names, signatures, and return types) satisfies the call sites you need, and no breaking changes are listed in the package changelog between the installed version and the project's minimum supported version.

## Create A PageObject

1. Define a Python class that inherits from `PageObject`.
2. Add `PAGE_TITLE` and `PAGE_URL` when the page has a canonical title or route.
3. Declare page elements as `UIObject` **class** attributes. Use a specific Browser locator string.
4. Keep each PageObject focused on one page or coherent region.

```python
from BrowserPOM import PageObject, UIObject
from robot.libraries.BuiltIn import library


@library
class MainPage(PageObject):
    PAGE_TITLE = "MainPage"
    PAGE_URL = "/index.html"
    search_bar = UIObject("//input[@id='searchBar']")
```

## Create A UIObject

1. Define a Python class that inherits from `UIObject`.
2. Declare nested child elements as **instance** attributes (not class attributes) and pass `parent=self` to each nested child.
3. Use UIObject subclasses for reusable components that appear in multiple pages.

```python
from BrowserPOM import UIObject


class SearchBar(UIObject):
    def __init__(self, locator: str) -> None:
        super().__init__(locator)
        self.submit_button = UIObject("//button[@type='submit']", parent=self)
        self.input_field = UIObject("//input", parent=self)
```

## Add Robot Keywords

1. Put reusable browser actions on the owning PageObject or UIObject.
2. Decorate public actions with `robot.api.deco.keyword` when they should be exposed as explicit Robot keywords.
3. Pass UIObjects to Browser Library calls as `str(ui_object)` so the complete parent-child locator is used.

```python
from robot.api.deco import keyword


class MainPage(PageObject):
    search_bar = UIObject("//input[@id='searchBar']")

    @keyword
    def enter_search(self, text: str) -> None:
        self.browser.type_text(str(self.search_bar), text)
```

## Failure Handling

To trigger Browser Library's registered failure keyword from a PageObject action:

1. Decorate the action with `@on_error_trigger` from `BrowserPOM.decorator`.
2. Register a failure keyword in Robot Framework, such as `Register Keyword To Run On Failure    Take Screenshot`.
3. Apply `@keyword` and `@on_error_trigger` to the action, in that order from top to bottom.

Do not assume the decorator handles failures by itself; the Robot failure keyword must be registered.

## Agent Workflow

1. Run `browserpom discover objects` and reuse a compatible local component instead of creating a new one.
2. Read the source file only if the compact output does not include required details.
3. Create or modify the PageObject or UIObject following the sections above.
4. Run the focused tests after making changes.
5. If discovery output is missing or incomplete, verify the Python environment, rerun from the project root, and inspect the referenced source file directly.
