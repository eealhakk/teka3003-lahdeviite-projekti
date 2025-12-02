*** Settings ***
Resource    resource.robot
Test Setup    Setup Database And ReferenceManager

*** Test Cases ***
Add Single Book And Verify
    Add Book To Database    BOOK1    Author One    Title One    2021    Publisher One    tag1,tag2
    Verify Reference In Database    BOOK1

Add Article And Verify
    Add Article To Database    ART1    Author Two    Title Two    Journal One    2022    1    10    tag3
    Verify Reference In Database    ART1

Add Inproceeding And Verify
    Add Inproceeding To Database    INP1    Author Three    Title Three    2023    INP Booktitle    tag4,tag5
    Verify Reference In Database    INP1
