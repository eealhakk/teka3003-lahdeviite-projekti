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

List Shows Multiple References
    Add Book To Database    BOOK2    A    T    2021    P
    Add Article To Database    ART1    A2    T2    J    2022    1    10
    Add Inproceeding To Database    INP1    A3    T3    2023    B

    Verify Reference In Database  BOOK2

Export Book To BibTeX
    Add Book    BOOK1    Author One    Title One    2021    Publisher One
    Export Bibtex File
    Bib File Should Exist
    Bib File Should Contain  @book{BOOK1,

