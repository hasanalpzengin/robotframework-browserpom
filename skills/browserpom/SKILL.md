---
name: browserpom
description: Create and use robotframework-browserpom PageObjects and UIObjects in Robot Framework projects.
---

# BrowserPOM Project Usage

Use this skill when creating, modifying, or consuming Python PageObjects and UIObjects with Robot Framework Browser.

## CLI Discovery

Before choosing or reusing an existing PageObject or UIObject, use the companion "browserpom-cli" skill to discover available classes in the project. The CLI reads the `pyproject.toml` configuration and outputs class names, source paths, and public methods for each existing PageObject or UIObject.

## Create A PageObject

1. Define a Python class that inherits from `PageObject`.
2. Add `PAGE_TITLE` and `PAGE_URL` when the page has a canonical title or route.
3. Declare page elements as `UIObject` attributes. Use a specific Browser locator string.
4. For reusable components, create a `UIObject` subclass and pass `parent=self` to every nested child.
5. Keep each PageObject or component focused on one page or coherent region.

```python
from BrowserPOM import PageObject, UIObject


class MainPage(PageObject):
	PAGE_TITLE = "MainPage"
	PAGE_URL = "/index.html"
	search_bar = UIObject("//input[@id='searchBar']")
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

## Use In Robot Framework

1. Import `BrowserPOM` and the Python module containing the PageObject as first library.
2. Alias the PageObject library with `AS` when the class name should be used as a stable namespace.
3. Open the browser in suite or test setup before calling PageObject keywords.
4. Call generated PageObject methods with the aliased name, and use Browser Library keywords for assertions and direct element operations.

```robot
*** Settings ***
Library    BrowserPOM
Library    demo/MainPage.py    AS    MainPage
Test Setup    Open Browser    https://automationbookstore.dev    headless=True

*** Test Cases ***
Search
	MainPage.Go To Page
	MainPage.Enter Search    text
	${count}=    MainPage.Get Tile Count
	Should Be Equal As Integers    ${count}    8
```

## Resolve Dynamic Elements

- Use `${page.component.item[0]}` to select by index.
- Use `${page.component.item["visible text"]}` to select by text.
- Use `${page.component.item.filter("hasText: 'visible text'")}` to filter an element collection.
- Chain child properties after any selection, for example `${MainPage.content_area.tile[1].title}`.
- Use `str()` in Python when passing a UIObject to a Browser Library keyword. Its string form contains the composed locator chain.

## Editor Variable Stubs

When Robot editor tooling reports POM variables as undefined:

1. Add a `variables.py` file only if the project needs an editor-visible variable mapping.
2. Register the helper in `robot.toml`:

```toml
variable-files = ["BrowserPOM.pom_stubs:demo/"]
```

3. Treat the values returned by `BrowserPOM.pom_stubs.get_variables("demo/")` as editor and linter placeholders, not runnable PageObject instances.

## Failure Handling

To trigger Browser Library's registered failure keyword from a PageObject action:

1. Decorate the action with `@on_error_trigger` from `BrowserPOM.decorator`.
2. Register a failure keyword in Robot Framework, such as `Register Keyword To Run On Failure    Take Screenshot`.
3. Apply `@keyword` and `@on_error_trigger` to the action, in that order from top to bottom.

Do not assume the decorator handles failures by itself; the Robot failure keyword must be registered.
