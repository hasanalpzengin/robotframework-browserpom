# robotframework-browserpom

[![PyPI version](https://img.shields.io/pypi/v/robotframework-browserpom.svg)](https://pypi.org/project/robotframework-browserpom/)

📖 **Documentation:** [https://hasanalpzengin.github.io/robotframework-browserpom](https://hasanalpzengin.github.io/robotframework-browserpom)

`robotframework-browserpom` is a [robotframework-browser](https://robotframework-browser.org/) library extension designed to simplify the creation of Page Objects. It provides an easy-to-use interface to define Page Object Models (POM) for browser automation with the Robot Framework, allowing for cleaner, maintainable, and reusable test automation code.

Heavily inspired by [robotframework-pageobjectlibrary](https://github.com/boakley/robotframework-pageobjectlibrary) repository which is built for usage with Selenium Library and not compatible with robotframework-browser.

## Features

- **Integration with Robot Framework Browser**: Seamlessly integrates with the `robotframework-browser` library.
- **Page Object Model Support**: Simplifies the creation and management of Page Objects in browser-based test automation.
- **Enhanced Readability**: Improves the maintainability of test automation by promoting a clean separation between test actions and page element interactions.

## Installation

To install `robotframework-browserpom`, you can use `poetry`:

```bash
poetry add robotframework-browserpom
```

Alternatively, to install in development mode (if you are contributing to the library):

poetry install

Dependencies

This project depends on the following libraries:

    Python 3.12 or above
    robotframework (>=7.1.0)
    robotframework-browser (>=18.0.0)

Development dependencies include:

    pytest for testing
    black for code formatting
    isort for sorting imports
    flake8 for linting
    mypy for static type checking
    pylint for additional linting checks
    coverage for test coverage reporting

Usage

To use robotframework-browserpom, create Page Objects by defining Python classes that represent the pages in your web application. These classes should contain methods that interact with the elements on the page.

Example:

```python
class MainPage(PageObject):
    """
    main page
    """
    PAGE_TITLE = "MainPage"
    PAGE_URL = "/index.html"

    tile = Tile("//li")
    search_bar: UIObject = UIObject("//input[@id='searchBar']")

    @keyword
    def enter_search(self, search):
        """Enter to search bar"""
        self.browser.type_text(str(self.search_bar), search)

    def get_tile_count(self):
        return self.browser.get_element_count(str(self.tile))

class Tile(UIObject):
        def __init__(self, locator: str, parent: UIObject | None = None):
                super().__init__(locator, parent=parent)
                self.price = UIObject("//p[contains(@id, '_price')]", parent=self)
                self.title = UIObject("//h2[contains(@id, '_title')]", parent=self)
                self.author = UIObject("//p[contains(@id, '_author')]", parent=self)
```
In this example the `parent` parameter is defined as `self` which makes the price, title and author a child of `Tile` POM.
Converting these UIObjects to the strings will generate a nested selector given as `parent_selector.. >> parent_selector >> child_selector`

Later, calling keywords
```robotframework
*** Settings ***
Library   Browser
Library   BrowserPOM
Library   demo/MainPage.py   AS  MainPage

Variables   demo/variables.py

Test Setup    Browser.Open Browser    https://automationbookstore.dev     headless=True

*** Test Cases ***
Search
    Go To Page    MainPage
    ${tileCount}=   MainPage.Get Tile Count
    Should Be Equal As Integers     ${tileCount}    8
    ${classes}=    Get Classes    ${MainPage.tile[0]}
    Get Text    ${MainPage.tile[1].title}    ==    Experiences of Test Automation
    Enter Search    text
    Should Be Equal    ${classes[0]}    ui-li-has-thumb
    Should Be Equal    ${classes[1]}    ui-first-child
```
>
> TIP:
> To remove the warnings from your editor create a variables.py file that imports the POM Libraries
>

## License

This project is licensed under the MIT License - see the LICENSE file for details.
Contributing

Contributions are welcome! Please fork this repository and submit a pull request with your changes.

Before submitting your pull request, make sure to:

    Follow the coding style conventions (Black for formatting, Flake8 for linting).
    Write tests for any new features or bug fixes.
    Update the documentation as needed.

Contact

For any questions or feedback, you can reach the project maintainer:

    Hasan Alp Zengin (hasanalpzengin@gmail.com)