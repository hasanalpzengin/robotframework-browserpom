# LLM Integration

This repository includes Agent Skills for LLM coding agents that work with `robotframework-browserpom`.

## Install The Skills

Run this command in the project where the skills should be available:

```bash
npx skills add hasanalpzengin/robotframework-browserpom
```

Follow the installer prompts to select the skills and installation scope. The repository provides these skills:

- `browserpom`: create, modify, and use Python `PageObject` and `UIObject` classes with Robot Framework Browser.
- `browserpom-cli`: discover available PageObjects and UIObjects before writing tests or adding components.

After installation, ask the LLM to use the relevant skill for the task. Use `browserpom-cli` first when the available PageObjects or UIObjects are unknown. Use `browserpom` when implementing or consuming those objects.

## Configure Discovery

The `browserpom-cli` skill requires discovery configuration in the project's `pyproject.toml`:

```toml
[tool.browserpom.discover]
paths = ["demo/"]
```

`paths` must be a non-empty list of existing project-relative directories or Python files. Run discovery from the directory containing this `pyproject.toml`:

```bash
browserpom discover pages
browserpom discover objects
```

Use `discover pages` to select a PageObject and its Robot keywords. Use `discover objects` to find reusable UIObject classes, child objects, locators, properties, and public methods.

## Recommended Agent Workflow

1. Install the skills with `npx skills add hasanalpzengin/robotframework-browserpom`.
2. Ensure the agent uses the same Python environment as the Robot Framework project.
3. Configure `[tool.browserpom.discover]` before asking the agent to run discovery commands.
4. Ask the agent to run `browserpom discover pages` before writing a Robot Framework test.
5. Ask the agent to run `browserpom discover objects` before adding a UIObject or component.
6. Ask the agent to use `browserpom` when creating PageObjects, nested UIObjects, custom keywords, or Robot Framework integrations.
7. Require the agent to run the focused Robot or Python tests after making changes.

The skills provide project-specific instructions. They do not replace the project's Python dependencies, Robot Framework Browser setup, test data, or test execution environment.
