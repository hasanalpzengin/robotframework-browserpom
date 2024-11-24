*** Settings ***
Library   Browser
Library   BrowserPOM
Library   demo/MainPage.py   AS  MainPage

Suite Setup     Browser.Open Browser    https://automationbookstore.dev     headless=True

*** Test Cases ***
Search
    Go To Page    MainPage
    ${tileCount}=   MainPage.Get Tile Count
    Should Be Equal As Integers     ${tileCount}    8






