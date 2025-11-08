# Usage

## Defining Page Objects

Create Python classes that inherit from `PageObject` and define UI elements as `UIObject` attributes.

```python
from BrowserPOM import PageObject, UIObject

class MainPage(PageObject):
    PAGE_TITLE = "MainPage"
    PAGE_URL = "/index.html"
    tile = UIObject("//li")
    search_bar = UIObject("//input[@id='searchBar']")
```

## Using in Robot Framework

```text
*** Settings ***
Library   BrowserPOM
Library   demo/MainPage.py   AS  MainPage
Test Setup    Open Browser    https://automationbookstore.dev     headless=True

*** Test Cases ***
Search
    MainPage.Go To Page
    ${tileCount}=   MainPage.Get Tile Count
```

## Editor integration: automatic POM variable stubs

Editors and language servers (for example RobotCode) can warn about
undefined variables referenced in Robot Framework tests. A common workaround is
to provide a `variables.py` file that imports or defines all POM libraries so
the IDE recognizes them. Keeping that file in sync with your POM modules is
tedious.

`BrowserPOM` includes a tiny helper module `BrowserPOM.pom_stubs` which
statically scans a folder for Python modules containing Page Object classes and
returns a mapping of class names to placeholder values. Because it uses the
`ast` module it doesn't import or execute your project code.

Example usage at runtime (Python):

```py
from BrowserPOM import pom_stubs

# returns something like {"MainPage": "MainPage", "Tile": "Tile"}
pom_stubs.get_variables("./demo/")
```

Registering the helper via `robot.toml` is convenient for editor tooling and
Robot runs. Add a `variable-files` entry, passing the folder that contains your
POM modules (path is relative to the repository root):

```toml
variable-files = ["BrowserPOM.pom_stubs:demo/"]
```

This instructs Robot tools to call `BrowserPOM.pom_stubs.get_variables("demo/")`
and use the returned mapping as variables for the project. The helper filters
for classes that inherit `PageObject` (best-effort detection for dotted or
parametrized base expressions).

Notes:

- Returned values are placeholders intended for editor/linter consumption and
    do not represent runnable objects.
- If you need richer metadata (file stems, class attributes, etc.) the helper
    can be extended; see `BrowserPOM/pom_stubs.py` for the current implementation.


---

# Advanced Usage

## 1. Hierarchical/Nested Page Objects
You can define page objects that contain other page objects or UI elements, reflecting the structure of your web page.

```python
class Content(UIObject):
    def __init__(self, locator, parent=None):
        super().__init__(locator, parent=parent)
        self.tile = Tile("xpath=//li", parent=self)

class Tile(UIObject):
    def __init__(self, locator, parent=None):
        super().__init__(locator, parent=parent)
        self.title = UIObject("//h2[contains(@id, '_title')]", parent=self)
```

## 2. Dynamic Element Access (Indexing, Text, Filtering)
- **By index:** `${MainPage.content_area.tile[0]}`
- **By text:** `${MainPage.content_area.tile["Experiences of Test Automation"].title}`
- **By filter:** `${MainPage.content_area.tile.filter("hasText: 'Experiences of Test Automation'").title}`

## 3. Chained/Nested Locators
The string representation of a UIObject automatically builds a full locator chain. Remember to wrap the UIObject in `str()` to get the selector string.
```text
str(${MainPage.content_area.tile[1].title})  # .ui-content >> xpath=//li >> nth=1 >> //h2[contains(@id, '_title')]
```

## 4. Custom Keywords in POM Classes
You can define custom Robot Framework keywords directly in your POM classes using the `@keyword` decorator:
```python
from robot.api.deco import keyword
class MainPage(PageObject):
    @keyword
    def enter_search(self, search):
        self.browser.type_text(str(self.search_bar), search)
```
Usage in Robot:
```text
Enter Search    text
```

## 5. Direct Python Method Calls in Robot
You can call Python methods on your page objects directly from Robot Framework:
```text
MainPage.Run    search_bar.search("This is a search")
```

## 6. Parent-Child Relationships
Each UIObject can have a parent, allowing for relative locators and encapsulation of sub-elements.

## 7. Locator Composition and Stringification
A `UIObject` instance returns the complete selector of the respective object. To use it with Browser Library keywords in python code, it must be encapsulated in `str()`. The `__str__` method in `UIObject` ensures that when you use a UIObject in a keyword or locator, it automatically resolves to the correct, fully-qualified locator string.

---

# Error Handling with Decorators

To ensure your Page Object keywords automatically run a keyword (such as taking a screenshot) on failure, decorate them with `on_error_trigger` from `BrowserPOM.decorator`:

```python
from BrowserPOM.decorator import on_error_trigger
from robot.api.deco import keyword

class MainPage(PageObject):
    @keyword
    @on_error_trigger
    def fail_keyword(self):
        text = self.browser.get_text(str(self.error_element))
```

Then, in your Robot Framework test, use:
```text
Register Keyword To Run On Failure    Take Screenshot
```
If you use `Take Screenshot`, a full screenshot will be taken automatically when an error occurs in a decorated keyword.

# Shared Page Object Models for Large Organizations

One of the key strengths of `robotframework-browserpom` is its support for scalable, maintainable automation architectures in large organizations:

## Benefits for Large Organizations
- **Centralized Page Object Libraries:** Define Page Object Models (POMs) in Python packages that can be versioned and shared across multiple teams or projects.
- **Consistency:** Enforce consistent element locators, naming, and test actions across all automation suites.
- **Reusability:** Teams can reuse and extend existing POMs, reducing duplication and maintenance effort.
- **Separation of Concerns:** Test logic is separated from UI structure, making it easier to update locators or add new features without breaking tests.
- **Collaboration:** Different teams (or even organizations) can contribute to and benefit from a shared repository of POMs, accelerating onboarding and knowledge transfer.

## How to Share POMs
- **Package your POMs:** Organize your POM classes in a Python package (or multiple packages) and publish them to a private PyPI server or share as a Git submodule.
- **Import in Robot Tests:** Teams can import and use these shared POMs in their Robot Framework test suites using the `Library` keyword.
- **Version Control:** Use semantic versioning and changelogs to manage updates and ensure compatibility across teams.

This approach enables large-scale, collaborative, and maintainable browser automation for enterprise environments.
