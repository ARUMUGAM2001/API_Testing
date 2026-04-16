import requests
from oauth import OAuth
import json
import time

BASE_URL="http://localhost:5000"

oauth = OAuth(
    client_id="telecom_client_id",
    client_secret="telecom_client_secret",
    base_url=BASE_URL,
)
oauth_token=oauth.get_header()
suspended_subscriber=None
def test_get_all_subscribers():
    response=requests.get(headers=oauth_token,url=f"{BASE_URL}/api/subscribers")
    assert response.status_code == 200,f"[STATUS_CODE]:{response.status_code},[RESPONSE_ERROR]:{response.text}"
    data=response.json()
    return data

def test_get_subscriber_id(payload:json,item_to_search:str)->list:
    subscriber_id= []
    if isinstance(payload,dict):
        if item_to_search in payload:
            subscriber_id.append(payload[item_to_search])
        for values in payload.values():
            subscriber_id.extend(test_get_subscriber_id(values,item_to_search))
    elif isinstance(payload,list):
        for p in payload:
            subscriber_id.extend(test_get_subscriber_id(p,item_to_search))
    return subscriber_id

def test_get_subscriber_by_id(subscriber_id:list)->list:
    all_ids=[]
    for sub_id in subscriber_id:
        response = requests.get(headers=oauth_token, url=f"{BASE_URL}/api/subscribers/{sub_id}",)
        assert response.status_code == 200,f"[STATUS_CODE]:{response.status_code},[RESPONSE_ERROR]:{response.text}"
        subscriber_found=response.json()
        data_two=test_get_subscriber_id(subscriber_found,"id")
        all_ids.extend(data_two)
    return all_ids

def test_create_subscriber(name:str)->str:
    names=[]
    phone_number=str(int(time.time()*1000))[-10:]
    json_body={

            "email": "test@telecom.com",
            "name": name,
            "phone": phone_number,
            "plan": "premium"

    }
    response=requests.post(json=json_body,headers=oauth_token,url=f"{BASE_URL}/api/subscribers")
    assert response.status_code == 201, f"[STATUS_CODE]:{response.status_code},[RESPONSE_ERROR]:{response.text}"
    subscriber_info=response.json()
    search_name=test_get_subscriber_id(subscriber_info,"name")
    names.extend(search_name)
    assert name in names
    print(f"[PASSED] Post-{name} subscriber created successfully")
    return response.json()["id"]

def test_update_subscriber(subscriber_to_modify:str):
    sub_id_to_modify=subscriber_to_modify
    json_body={
            "email": "new@telecomnew.com",
            "name": "Arumugam four",
            "plan": "basic"

    }
    response=requests.put(
        url=f"{BASE_URL}/api/subscribers/{sub_id_to_modify}",
        headers=oauth_token,
        json=json_body
    )
    assert response.status_code == 200, f"[STATUS_CODE]:{response.status_code},[RESPONSE_ERROR]:{response.text}"
    print(f"[PASSED] PUT-{sub_id_to_modify} subscriber updated successfully")

def test_suspend_subscriber(subscriber_to_suspend:str) ->str:
    sub_id_to_suspend=subscriber_to_suspend
    response = requests.put(
        url=f"{BASE_URL}/api/subscribers/{sub_id_to_suspend}/suspend",
        headers=oauth_token
    )
    assert response.status_code == 200, f"[STATUS_CODE]:{response.status_code},[RESPONSE_ERROR]:{response.text}"
    print(f"[PASSED] PUT-{sub_id_to_suspend} subscriber got suspended successfully")
    return sub_id_to_suspend

def test_activate_subscriber(subscriber_to_activate:str) ->str:
    sub_id_to_activate = subscriber_to_activate
    response = requests.put(
        url=f"{BASE_URL}/api/subscribers/{sub_id_to_activate}/activate",
        headers=oauth_token
    )
    assert response.status_code == 200, f"[STATUS_CODE]:{response.status_code},[RESPONSE_ERROR]:{response.text}"
    print(f"[PASSED] PUT-{sub_id_to_activate} subscriber got activated successfully")
    return subscriber_to_activate

def test_get_usage(subscriber_id:str) ->json:
    response=requests.get(url=f"{BASE_URL}/api/subscribers/{subscriber_id}/usage",headers=oauth_token)
    assert response.status_code==200,f"[STATUS_CODE]:{response.status_code},[RESPONSE_ERROR]:{response.text}"
    return response.json()

def test_delete_subscriber(subscriber_id:str) :
    response=requests.delete(url=f"{BASE_URL}/api/subscribers/{subscriber_id}",headers=oauth_token)
    assert response.status_code == 200, f"[STATUS_CODE]:{response.status_code},[RESPONSE_ERROR]:{response.text}"
    return print(f"[PASSED]delete subscriber {subscriber_id} successfully")

if __name__=="__main__":
    #create subscriber
    new_subscriber=test_create_subscriber("Test User Three")
    data=test_get_all_subscribers()
    entire_data=test_get_subscriber_id(data,item_to_search="id")
    id_search=test_get_subscriber_by_id(entire_data)
    assert entire_data==id_search, f"[FAIL] ID mismatch: {entire_data} != {id_search}"
    print(f"[PASS] All IDs verified: {id_search}")
    #modify newly created subscriber info
    test_update_subscriber(new_subscriber)
    #suspend subscriber
    suspended_subscriber=test_suspend_subscriber(new_subscriber)
    print(f"Suspended subscriber: {suspended_subscriber}")
    #activate subscriber
    activated_subscriber=test_activate_subscriber(suspended_subscriber)
    print(f"Activated subscriber: {activated_subscriber}")
    #usage record
    get_usage=test_get_usage(activated_subscriber)
    item_to_search=["calls_min","data_mb"]
    usage_details={}
    for item in item_to_search:
        for value in test_get_subscriber_id(get_usage,item):
            usage_details[item]=value
    print(f"Usage details: {usage_details}")
    #delete subscriber
    test_delete_subscriber(activated_subscriber)

