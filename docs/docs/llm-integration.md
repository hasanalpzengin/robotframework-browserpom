# LLM Integration

This repository includes Agent Skills for LLM coding agents that work with `robotframework-browserpom`.

## Install The Skills

Run this command in the project where the skills should be available:

```bash
npx skills add hasanalpzengin/robotframework-browserpom
```

Follow the installer prompts to select the skills and installation scope. The repository provides these skills:

- `browserpom-create-robot-tests`: discover PageObjects and write Robot Framework tests.
- `browserpom-create-pageobjects`: discover existing UIObjects and create or modify `PageObject` and `UIObject` classes.

After installation, ask the LLM to use the relevant skill for the task. Use `browserpom-create-robot-tests` when writing or modifying Robot tests. Use `browserpom-create-pageobjects` when creating or extending Python PageObject or UIObject classes.

## Configure Discovery

Both skills require a `[tool.browserpom.discover]` section in the project's `pyproject.toml` before running discovery commands. If that section is missing, the CLI prints a descriptive error that agents can relay to users to prompt configuration. See each skill for the full configuration reference and usage guidance.

## Recommended Agent Workflow

1. Install the skills with `npx skills add hasanalpzengin/robotframework-browserpom`.
2. Ensure the agent uses the same Python environment as the Robot Framework project.
3. Configure `[tool.browserpom.discover]` in `pyproject.toml` before asking the agent to run discovery commands.
4. Ask the agent to use `browserpom-create-robot-tests` before writing a Robot Framework test.
5. Ask the agent to use `browserpom-create-pageobjects` before adding a UIObject or component.
6. Ask the agent to use `browserpom-create-pageobjects` when creating PageObjects, nested UIObjects, or custom keywords.
7. Require the agent to run the focused Robot or Python tests after making changes.

The skills provide project-specific instructions. They do not replace the project's Python dependencies, Robot Framework Browser setup, test data, or test execution environment.
