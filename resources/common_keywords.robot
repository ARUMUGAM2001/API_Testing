*** Settings ***
Library    ../libraries/TelecomAPILibrary.py
Resource   ../resources/variables.robot

*** Keywords ***
Initialize API
    Setup API Session
    ...    ${BASE_URL}
    ...    ${CLIENT_ID}
    ...    ${CLIENT_SECRET}
    

