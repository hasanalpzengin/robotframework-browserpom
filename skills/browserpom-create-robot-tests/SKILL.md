---
name: browserpom-create-robot-tests
description: Discover available PageObjects and write Robot Framework tests using robotframework-browserpom.
---

# BrowserPOM — Write Robot Framework Tests

Use this skill when writing or modifying Robot Framework tests that consume `PageObject` classes from a `robotframework-browserpom` project.

## Discover Available PageObjects

Before writing a test, run discovery to see which PageObjects exist:

```bash
browserpom discover pages
```

This requires a `[tool.browserpom.discover]` section in the project's `pyproject.toml`. If the section is missing the CLI prints a descriptive error — add the section and retry:

```toml
[tool.browserpom.discover]
paths = ["demo/"]
```

Run the command from the directory containing `pyproject.toml` and in the same Python environment as the tests.

### Interpret Page Output

Read output as blank-line-separated class blocks. Each block starts with `ClassName: path/to/file.py`.

- `url:` is a route hint.
- Indented arrows describe traversable child objects.
- Trailing signatures are public PageObject keywords or properties.

Read the PageObject source file only if the compact output does not include required details.

## Use In Robot Framework

1. Import `BrowserPOM` and the Python module containing the PageObject. Follow the import ordering required by the project's linter (typically: built-in libraries first, then external libraries such as `BrowserPOM`, then project libraries).
2. Alias the PageObject library with `AS` when the class name should be used as a stable namespace.
3. Open the browser in suite or test setup before calling PageObject keywords. Prefer `New Page` over `Open Browser` to avoid deprecation warnings.
4. Call generated PageObject keywords with the aliased name, and use Browser Library keywords for assertions and direct element operations.

```robot
*** Settings ***
Library    BrowserPOM
Library    demo/MainPage.py    AS    MainPage
Test Setup    New Page    https://automationbookstore.dev

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

## Editor Variable Stubs

When Robot editor tooling reports POM variables as undefined:

1. Check whether the project already registers `BrowserPOM.pom_stubs` in `robot.toml`. If it does, no further action is needed — reuse the existing stub registration.
2. Only add a `variables.py` file if no editor stubs exist **and** the developer explicitly confirms one is needed.
3. Register the helper in `robot.toml`:

```toml
variable-files = ["BrowserPOM.pom_stubs:demo/"]
```

4. Treat the values returned by `BrowserPOM.pom_stubs.get_variables("demo/")` as editor and linter placeholders, not runnable PageObject instances.

## Agent Workflow

1. Run `browserpom discover pages` and select the PageObject whose route and keywords match the scenario.
2. Read the PageObject source file only if the compact output does not include required details.
3. Write the Robot test, following the import and setup guidance above.
4. Run the focused tests after making changes.
5. If discovery output is missing or incomplete, verify the Python environment, rerun from the project root, and inspect the referenced source file directly.
