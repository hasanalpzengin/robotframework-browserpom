*** Settings ***
Library   Browser
Library   BrowserPOM
Library   demo/MainPage.py   AS  MainPage

Test Setup    Browser.Open Browser    https://automationbookstore.dev     headless=True

Variables    demo/variables.py

*** Test Cases ***
Search
    Go To Page    MainPage
    ${tileCount}=   MainPage.Get Tile Count
    Should Be Equal As Integers     ${tileCount}    8
    ${classes}=    Get Classes    ${MainPage.content_area.tile[0]}
    Get Text    ${MainPage.content_area.tile[1].title}    ==    Experiences of Test Automation
    Get Text    ${MainPage.content_area.tile["Experiences of Test Automation"].title}    ==    Experiences of Test Automation
    Enter Search    text
    MainPage.Run    search_bar.search("This is a search")
    Should Be Equal    ${classes[0]}    ui-li-has-thumb
    Should Be Equal    ${classes[1]}    ui-first-child
    Should Be Equal As Strings    ${MainPage.content_area.tile[1].title}    .ui-content >> xpath=//li >> nth=1 >> //h2[contains(@id, '_title')]
