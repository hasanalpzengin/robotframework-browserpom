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
The string representation of a UIObject automatically builds a full locator chain:
```text
${MainPage.content_area.tile[1].title}  # .ui-content >> xpath=//li >> nth=1 >> //h2[contains(@id, '_title')]
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
The `__str__` method in `UIObject` ensures that when you use a UIObject in a keyword or locator, it automatically resolves to the correct, fully-qualified locator string.

---
For more, see the [Examples](/examples) section. 