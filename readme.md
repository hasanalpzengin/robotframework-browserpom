# robotframework-browserpom

[![PyPI version](https://img.shields.io/pypi/v/robotframework-browserpom.svg)](https://pypi.org/project/robotframework-browserpom/)

📖 **Documentation:** [https://hasanalpzengin.github.io/robotframework-browserpom](https://hasanalpzengin.github.io/robotframework-browserpom)

`robotframework-browserpom` is a small extension for `robotframework-browser` that
makes it easy to define Page Object Models (POMs) for browser-based Robot
Framework tests. It provides helpers and conventions for building readable,
reusable page objects and wiring them into Robot tests.

## Features

- **Integration with Robot Framework Browser**: Seamlessly integrates with the `robotframework-browser` library.
- **Page Object Model Support**: Simplifies the creation and management of Page Objects in browser-based test automation.
- **Enhanced Readability**: Improves the maintainability of test automation by promoting a clean separation between test actions and page element interactions.

## Installation

To install `robotframework-browserpom` use `poetry`:

```bash
poetry add robotframework-browserpom
```

For development / contributing:

```bash
poetry install
```

## Dependencies

- Python 3.12 or above
- robotframework (>=7.1.0)
- robotframework-browser (>=18.0.0)

Development dependencies commonly used by contributors:

- pytest (testing)
- black (formatting)
- isort (import sorting)
- flake8 / pylint (linting)
- mypy (static type checking)
- coverage (coverage reports)

## Quick usage

Create Page Objects as Python classes and use them from Robot Framework tests. Example:

```python
class MainPage(PageObject):
  PAGE_TITLE = "MainPage"
  PAGE_URL = "/index.html"

  tile = Tile("//li")
  search_bar: UIObject = UIObject("//input[@id='searchBar']")

  @keyword
  def enter_search(self, search):
    self.browser.type_text(str(self.search_bar), search)
```

Then import the POM library in Robot tests:

```robot
*** Settings ***
Library   BrowserPOM
Library   demo/MainPage.py   AS  MainPage

Test Setup    Browser.Open Browser    https://automationbookstore.dev     headless=True
```
# robotframework-browserpom

[![PyPI version](https://img.shields.io/pypi/v/robotframework-browserpom.svg)](https://pypi.org/project/robotframework-browserpom/)

📖 **Documentation:** [https://hasanalpzengin.github.io/robotframework-browserpom](https://hasanalpzengin.github.io/robotframework-browserpom)

`robotframework-browserpom` is a small extension for `robotframework-browser` that
makes it easy to define Page Object Models (POMs) for browser-based Robot
Framework tests. It provides helpers and conventions for building readable,
reusable page objects and wiring them into Robot tests.

## Editor / linter integration: the variables problem

Many editors and language servers (e.g., RobotCode / Robot Framework IntelliSense)
warn when variables referenced by Robot Framework tests are not defined. The
common workaround is to maintain a `variables.py` that imports or defines the
POM libraries so the IDE recognizes them. Maintaining that file by hand is
tedious — every time you add a new Page Object module you must update the
variables file.

To avoid this manual step, `BrowserPOM` ships a tiny utility module that
statically scans a Python package/folder for Page Object classes and returns
dummy variable values for them. Because it uses Python's `ast` module no
project code is executed — it's safe and fast.

## The `pom_stubs` helper

`BrowserPOM.pom_stubs.get_variables(base_path)` will scan `base_path` for
`.py` modules and return a mapping of class names for classes that inherit
from `PageObject`. The returned mapping can be used as a Robot variables file
source (via `robot.toml` or the `--variablefile` CLI option).

Example behavior:

```py
from BrowserPOM import pom_stubs

# returns something like {"MainPage": "MainPage", "Tile": "Tile"}
pom_stubs.get_variables("./demo/")
```

This is intentionally minimal: the actual variable values are irrelevant for
editor intellisense — they just need to exist so the linter stops complaining.

If you prefer, the helper may be extended to return more information (file
stems, class attributes, dummy instances, etc.).

## Usage via `robot.toml`

You can register the helper as a variable-file in `robot.toml` so your editor or
Robot runner picks it up automatically. Example `robot.toml`:

```toml
variable-files = ["BrowserPOM.pom_stubs:demo/"]
```

That tells the Robot tools to call `BrowserPOM.pom_stubs.get_variables("demo/")`
and use the returned mapping as variables for the project. The argument is the
path to the folder containing your POM modules (relative to the project root).

Alternatively you can pass the helper directly on the Robot CLI:

```bash
# optional example shown for documentation only
robot --variablefile BrowserPOM.pom_stubs:demo/ tests/
```

## Example Page Object

Define your page objects as normal — inherit from `PageObject` and add your
members and keywords:

```python
class MainPage(PageObject):
    PAGE_TITLE = "MainPage"
    PAGE_URL = "/index.html"

    tile = Tile("//li")
    search_bar: UIObject = UIObject("//input[@id='searchBar']")

    @keyword
    def enter_search(self, search):
        self.browser.type_text(str(self.search_bar), search)

    def get_tile_count(self):
        return self.browser.get_element_count(str(self.tile))
```

## Notes and limitations

- The helper uses `ast` and does not import or execute any project code.
- It currently includes classes that inherit from `PageObject` (best-effort
  detection for dotted or parametrized base expressions).
- The returned variable values are dummy placeholders intended for editor
  tooling only. If you need richer stubs (e.g., mapping to file stems or class
  metadata) we can extend the helper.

## Contributing

Contributions are welcome; please follow the repository coding guidelines and
add tests for new behavior.

## License

This project is licensed under the MIT License - see the LICENSE file for
details.