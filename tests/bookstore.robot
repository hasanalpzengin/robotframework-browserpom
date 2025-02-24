*** Settings ***
Library   Browser
Library   BrowserPOM
Library   demo/MainPage.py   AS  MainPage

Test Setup    Browser.Open Browser    https://automationbookstore.dev     headless=True

*** Test Cases ***
Search
    Go To Page    MainPage
    ${tileCount}=   MainPage.Get Tile Count
    Should Be Equal As Integers     ${tileCount}    8
    ${classes}=    Get Classes    ${MainPage.tile} >> xpath=../li[1]
    Should Be Equal    ${classes[0]}    ui-li-has-thumb
    Should Be Equal    ${classes[1]}    ui-first-child
