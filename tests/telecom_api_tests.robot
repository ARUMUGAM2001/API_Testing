*** Settings ***
Library     ../libraries/TelecomAPILibrary.py
Resource    ../resources/common_keywords.robot
Resource    ../resources/variables.robot
Suite Setup    Initialize API
Test Tags    API    regression

*** Test Cases ***
TC-01 GET All Subscribers
    ${data}=    Get All Subscribers
    ${id_info}=    Extract Field From Response    ${data}    id
    Should Not Be Empty    ${id_info}
    Log    ${id_info}    console=True

TC-02 Create New Subscriber
    ${new_sub_id}=    Create Subscriber    ${SUB_NAME}
    Set Suite Variable    ${CREATED_SUB_ID}    ${new_sub_id}
    Should Not Be Empty    ${new_sub_id}
    Should Be Equal As Strings    ${new_sub_id}    ${CREATED_SUB_ID}
    Log    ${new_sub_id}    console=True

TC-03 Get Subscriber By ID
    ${sub_search_response}=    Get Subscriber By ID    ${CREATED_SUB_ID}
    ${id_info}=    Extract Field From Response    ${sub_search_response}    id
    Should Not Be Empty    ${id_info}
    Should Be Equal As Strings    ${CREATED_SUB_ID}   ${sub_search_response}[id]

TC-04 Update Subscriber
    ${modified_subscriber}=    Update Subscriber    
    ...    ${CREATED_SUB_ID}
    ...    new_name
    ...    updated@mail.com
    ...    basic
    Should Not Be Empty    ${modified_subscriber}
    ${id_info}=    Extract Field From Response    ${modified_subscriber}    name
    Log    ${id_info}    console=True
    
TC-05 Suspend Subscriber
    ${suspend_sub_id}=    Suspend Subscriber    ${CREATED_SUB_ID}
    Should Not Be Empty    ${suspend_sub_id}
    Should Be Equal As Strings    ${suspend_sub_id}    ${CREATED_SUB_ID}
    Log    ${suspend_sub_id} ${CREATED_SUB_ID}    console=True

    