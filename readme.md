# robotframework-browserpom

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
from robot.api.deco import keyword

from BrowserPOM.pageobject import PageObject


class MainPage(PageObject):
    """
    main page
    """
    PAGE_TITLE = "MainPage"
    PAGE_URL = "/index.html"

    _locators = {
        "tile": {
            "skeleton": "//li",
            "price_label": "//li//p[2]",
            "title": "//li//h2",
            "author": "//li//p[1]"
        },
        "search_bar": "input[@id='searchBar']"
    }

    @keyword
    def enter_search(self, search):
        """Enter to search bar"""
        self.browser.type_text(self.locator.search_bar, search)

    def get_tile_count(self):
        return self.browser.get_element_count(self.locator.get("tile").get("skeleton"))
```

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