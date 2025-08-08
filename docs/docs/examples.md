# Examples

## Example Page Object (Python)
```python
class Tile(UIObject):
    def __init__(self, locator: str, parent: UIObject | None = None):
        super().__init__(locator, parent=parent)
        self.price = UIObject("//p[contains(@id, '_price')]", parent=self)
        self.title = UIObject("//h2[contains(@id, '_title')]", parent=self)
        self.author = UIObject("//p[contains(@id, '_author')]", parent=self)
```

## Example Test Case (Robot Framework)
```text
*** Test Cases ***
Search
    MainPage.Go To Page
    ${tileCount}=   MainPage.Get Tile Count
    Should Be Equal As Integers     ${tileCount}    8
    ${classes}=    Get Classes    ${MainPage.content_area.tile[0]}
    Get Text    ${MainPage.content_area.tile[1].title}    ==    Experiences of Test Automation
    Enter Search    text
    Should Be Equal    ${classes[0]}    ui-li-has-thumb
```

## Hierarchical/Nested Page Objects
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

## Dynamic Element Access
- **By index:**
  ```text
  ${MainPage.content_area.tile[0]}
  ${MainPage.content_area.tile[1].title}
  ```
- **By text:**
  ```text
  ${MainPage.content_area.tile["Experiences of Test Automation"].title}
  ```
- **By filter:**
  ```text
  ${MainPage.content_area.tile.filter("hasText: 'Experiences of Test Automation'").title}
  ```

## Chained/Nested Locators
```text
${MainPage.content_area.tile[1].title}  # .ui-content >> xpath=//li >> nth=1 >> //h2[contains(@id, '_title')]
```

## Custom Keywords in POM Classes
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

## Direct Python Method Calls in Robot
```text
MainPage.Run    search_bar.search("This is a search")
```

## Full Example Test Case
```text
*** Test Cases ***
Search
    MainPage.Go To Page
    ${tileCount}=   MainPage.Get Tile Count
    Should Be Equal As Integers     ${tileCount}    8
    ${classes}=    Get Classes    ${MainPage.content_area.tile[0]}
    Get Text    ${MainPage.content_area.tile[1].title}    ==    Experiences of Test Automation
    Get Text    ${MainPage.content_area.tile["Experiences of Test Automation"].title}    ==    Experiences of Test Automation
    Get Text    ${MainPage.content_area.tile.filter("hasText: 'Experiences of Test Automation'").title}    ==    Experiences of Test Automation
    Enter Search    text
    MainPage.Run    search_bar.search("This is a search")
    Should Be Equal    ${classes[0]}    ui-li-has-thumb
    Should Be Equal    ${classes[1]}    ui-first-child
    Should Be Equal As Strings    ${MainPage.content_area.tile[1].title}    .ui-content >> xpath=//li >> nth=1 >> //h2[contains(@id, '_title')]
```

## Error Handling with Decorators

You can use the `on_error_trigger` decorator to enable integration with the `Register Keyword To Run On Failure` keyword of the Browser library. This does not automatically implement error handling by itself, but allows your Page Object keywords to trigger the registered failure keyword (such as taking a screenshot) when an error occurs.

```python
from BrowserPOM.decorator import on_error_trigger
from robot.api.deco import keyword

class MainPage(PageObject):
    @keyword
    @on_error_trigger
    def fail_keyword(self):
        text = self.browser.get_text(str(self.error_element))
```

In your Robot Framework test, register a keyword to run on failure:
```text
Register Keyword To Run On Failure    Take Screenshot
```
If you use `Take Screenshot`, a full screenshot will be taken automatically when an error occurs in a decorated keyword.

For more, see the [Usage](/usage) section.
