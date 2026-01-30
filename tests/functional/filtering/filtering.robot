*** Settings ***
Documentation       Bug retest: locators containing single quotes led to "Syntax Error" when trying to filter for text,
...                 for example `${POM.electronics["Laptop"]}`

Library             BrowserPOM
Library             ./POM.py

Test Setup          New Page    file:///${CURDIR}/filtering.html


*** Test Cases ***
Filtering by index
    Get Attribute    ${POM.electronics[0]}    id    equals    item-1
    Get Attribute    ${POM.electronics[1]}    id    equals    item-3

Filtering by text content
    Get Attribute    ${POM.electronics["Laptop"]}    id    equals    item-1
    Get Attribute    ${POM.books["Python Programming Guide"]}    id    equals    item-2
