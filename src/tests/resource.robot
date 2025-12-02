*** Settings ***
Library    ../ReferenceManagerLibrary.py

*** Keywords ***
Setup Database And ReferenceManager
    Setup Database

Add Book To Database
    [Arguments]    ${key}    ${author}    ${title}    ${year}    ${publisher}    ${tags}=None
    Add Book    ${key}    ${author}    ${title}    ${year}    ${publisher}    ${tags}

Add Article To Database
    [Arguments]    ${key}    ${author}    ${title}    ${journal}    ${year}    ${volume}    ${pages}    ${tags}=None
    Add Article    ${key}    ${author}    ${title}    ${journal}    ${year}    ${volume}    ${pages}    ${tags}

Add Inproceeding To Database
    [Arguments]    ${key}    ${author}    ${title}    ${year}    ${booktitle}    ${tags}=None
    Add Inproceeding    ${key}    ${author}    ${title}    ${year}    ${booktitle}    ${tags}

Verify Reference In Database
    [Arguments]    ${key}
    ${listing}=    Listaa
    Should Contain    ${listing}    ${key}
