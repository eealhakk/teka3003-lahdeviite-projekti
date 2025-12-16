*** Settings ***
Resource    resource.robot
Test Setup    Setup Database And ReferenceManager

*** Test Cases ***
Add Single Book And Verify
    Add Book To Database    Martin09    Martin    Clean Code: A Handbook of Agile Software Craftsmanship    2008    Prentice Hall    Agile,Development
    Verify Reference In Database    Martin09

Add Article And Verify
    Add Article To Database    CBH91    Allan Collins and John Seeley Brown and Ann Holum    Cognitive apprenticeship: making thinking visible    American Educator    1991    6    38--46
    Verify Reference In Database    CBH91

Add Inproceeding And Verify
    Add Inproceeding To Database    VPL11    Vihavainen, Arto and Paksula, Matti and Luukkainen, Matti    Extreme Apprenticeship Method in Teaching Programming for Beginners    2011    SIGCSE    Eeppinen,klassikko
    Verify Reference In Database    VPL11

List Shows Multiple References
    Add Book To Database    Martin09    Martin    Clean Code: A Handbook of Agile Software Craftsmanship    2008    Prentice Hall    Agile,Development
    Add Article To Database    CBH91    Allan Collins and John Seeley Brown and Ann Holum    Cognitive apprenticeship: making thinking visible    American Educator    1991    6    38--46
    Add Inproceeding To Database    VPL11    Vihavainen, Arto and Paksula, Matti and Luukkainen, Matti    Extreme Apprenticeship Method in Teaching Programming for Beginners    2011    SIGCSE    Eeppinen,klassikko

    Verify Reference In Database  CBH91

Delete Reference Flow
    Add Book To Database    DEL1    Author X    Title X    2020    Pub X    tag1
    Verify Reference In Database    DEL1
    Delete Reference From Database    DEL1
    Verify Reference Not In Database    DEL1

Export Book To BibTeX
    Add Book    Martin09    Martin    Clean Code: A Handbook of Agile Software Craftsmanship    2008    Prentice Hall    Agile,Development
    Export Bibtex File
    Bib File Should Exist
    Bib File Should Contain  @book{Martin09,

Add Article By DOI And Verify
    Add Article By DOI To Database    10.1080/10509585.2015.1092083    DOI1    DOI,testaus
    Verify Reference In Database    DOI1
