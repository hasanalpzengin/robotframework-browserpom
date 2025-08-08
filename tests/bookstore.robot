*** Settings ***
Library   BrowserPOM
Library   demo/MainPage.py   AS  MainPage

Test Setup    Open Browser    https://automationbookstore.dev     headless=True

Variables    demo/variables.py

*** Test Cases ***
Search
    MainPage.Go To Page
    ${tileCount}=   MainPage.Get Tile Count
    Should Be Equal As Integers     ${tileCount}    8
    ${classes}=    Get Classes    ${MainPage.content_area.tile[0]}
    Get Text    ${MainPage.content_area.tile[1].title}    ==    Experiences of Test Automation
    Get Text    ${MainPage.content_area.tile["Experiences of Test Automation"].title}    ==    Experiences of Test Automation
    Get Text    ${MainPage.content_area.tile.filter("hasText: 'Experiences of Test Automation'").title}    ==    Experiences of Test Automation
    Enter Search    text
    MainPage.Run    search_bar.search("This is a search")
    Should Be Equal    ${classes[0]}    ui-li-has-thumb
    Should Be Equal    ${classes[1]}    ui-first-child
    Should Be Equal As Strings    ${MainPage.content_area.tile[1].title}    .ui-content >> xpath=//li >> nth=1 >> //h2[contains(@id, '_title')]

On Error Register
    Register Keyword To Run On Failure    Take Screenshot
    MainPage.Go To Page
    Run Keyword And Expect Error    STARTS: TimeoutError:    MainPage.Fail Keyword