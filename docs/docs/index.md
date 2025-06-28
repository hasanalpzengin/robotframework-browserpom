# robotframework-browserpom

[![PyPI version](https://img.shields.io/pypi/v/robotframework-browserpom.svg)](https://pypi.org/project/robotframework-browserpom/)

A Page Object Model extension for [Robot Framework Browser](https://robotframework-browser.org/).

## Introduction

`robotframework-browserpom` simplifies the creation of Page Objects for browser automation with Robot Framework. It enables you to define Python classes as page objects, making your test code cleaner, more maintainable, and reusable.

- **Integrates with Robot Framework Browser**
- **Supports Page Object Model (POM) pattern**
- **Promotes clean, maintainable test code**

## Quickstart

1. **Install the library:**
   ```bash
   poetry add robotframework-browserpom
   # or for development:
   poetry install
   ```
2. **Define your Page Objects in Python:**
   ```python
   from BrowserPOM import PageObject, UIObject
   class MainPage(PageObject):
       PAGE_TITLE = "MainPage"
       PAGE_URL = "/index.html"
       tile = UIObject("//li")
   ```
3. **Use in your Robot Framework tests:**
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
For more details, see the [Usage](/usage) and [Examples](/examples) sections.
