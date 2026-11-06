*** Settings ***
Documentation       UIObject iteration preserves subclass behavior and parent locators.
Library             BrowserPOM
Library             Collections
Library             ./IterationPage.py
Test Setup          New Page    file:///${CURDIR}/iteration.html
Test Teardown       Close Page
Suite Teardown      Close Browser

*** Test Cases ***
Robot iteration yields typed UIObjects in matching order
    ${labels}=    Create List
    FOR    ${row}    IN    @{IterationPage.rows}
        Get Text    ${row.label_object}    equals    ${row.label}
        Append To List    ${labels}    ${row.label}
    END
    ${expected}=    Create List    First    Second    Third
    Lists Should Be Equal    ${labels}    ${expected}

Python iteration uses the same Browser connection
    ${labels}=    IterationPage.Read Labels In Python
    ${expected}=    Create List    First    Second    Third
    Lists Should Be Equal    ${labels}    ${expected}

No matches produce an empty loop
    FOR    ${row}    IN    @{IterationPage.missing}
        Fail    No UIObjects should be yielded
    END

Repeated iteration queries the current matches
    ${initial}=    Create List    @{IterationPage.rows}
    Length Should Be    ${initial}    3
    Evaluate JavaScript    ${IterationPage.rows[0]}    (element) => element.remove()
    ${remaining}=    Create List    @{IterationPage.rows}
    Length Should Be    ${remaining}    2
    Should Be Equal    ${remaining[0].label}    Second
