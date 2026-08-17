---
name: browserpom-cli
description: Discover PageObjects and UIObjects available to a robotframework-browserpom project.
---

# BrowserPOM Discovery CLI

Use this skill before writing Robot Framework tests or adding PageObject/UIObject classes when the project exposes the `browserpom` command.

## Configure Discovery

Before running either discovery command, add a `[tool.browserpom.discover]` section to the project's `pyproject.toml`. The `paths` value is required, must be a non-empty TOML list, and must contain paths that exist relative to the project root:

```toml
[tool.browserpom.discover]
paths = ["demo/"]
```

Use a directory to scan all Python files below it, or provide a specific Python file:

```toml
[tool.browserpom.discover]
paths = ["src/pages/", "src/components/common.py"]
```

The CLI reads `pyproject.toml` from the current working directory. Run it from the directory containing that file. If the section is missing, add it; if `paths` is empty or a configured target does not exist, correct the TOML path before retrying.

## Commands

Run commands from the project root and in the same Python environment as the tests:

```bash
browserpom discover pages
browserpom discover objects
```

Use `discover pages` to choose a PageObject for a Robot test. Use `discover objects` to find reusable UIObject classes, locators, children, properties, and public methods before implementing a component.

## Interpret Output

Read output as blank-line-separated class blocks. Each block starts with `ClassName: path/to/file.py`.

- In page output, `url:` is a route hint, indented arrows describe traversable child objects, and trailing signatures are public PageObject keywords or properties.
- In object output, child entries include locator expressions. Use the source path to resolve duplicate class names.
- Discovery is static and best effort. Dynamic class creation, unusual decorators, import failures, or inaccessible packages can produce incomplete results.

## Agent Workflow

1. Run `browserpom discover pages` before authoring a test and select the PageObject whose route and keywords match the scenario.
2. Read that PageObject source file when the compact output does not show required action details.
3. Run `browserpom discover objects` before adding a UIObject and reuse a compatible local component instead of duplicating it.
4. Prefer local source objects when changing behavior. Use installed-package objects only after checking that their version and API fit the project.
5. If a result is missing or incomplete, verify the Python environment, rerun from the project root, and inspect the referenced source file directly.
