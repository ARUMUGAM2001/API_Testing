import requests

BASE_URL="https://jsonplaceholder.typicode.com"
def test_get():
    """GET - Getting existing data"""
    response=requests.get(f"{BASE_URL}/posts/1")
    #status code
    assert response.status_code==200
    data=response.json()
    #key check
    assert "title" in data
    #value check
    assert data["id"]==1
    print(f"[PASSED][GET]: {data['title']}")

def test_post():
    """POST - Create New Data"""
    payload = {
        "title": "SDET Practice Post",
        "body": "Learning API automation",
        "userId": 1
    }
    response=requests.post(url=f"{BASE_URL}/posts", json=payload)
    assert response.status_code==201

    data=response.json()
    assert data["title"] == "SDET Practice Post"
    assert "id" in data
    print(f"[PASSED][POST]: {data['title']}")

def test_put():
    """PUT complete update"""
    payload = {
        "id": 1,
        "title": "Updated Title",
        "body": "Updated body",
        "userId": 1
    }

    response=requests.put(f"{BASE_URL}/posts/1", json=payload)
    assert response.status_code==200
    data=response.json()
    assert data["title"] == "Updated Title"
    assert "id" in data
    print(f"[PASSED][PUT]: {data['title']}")

def test_delete():
    """DELETE Specific Item"""
    response=requests.delete(f"{BASE_URL}/posts/1")
    assert response.status_code in [200,204]
    print(f"[PASSED][DELETE]: {response.json()}")

def test_all_get():
    #challenge1
    response=requests.get(f"{BASE_URL}/posts?userId=1")
    # challenge2
    assert response.elapsed.total_seconds()<1,f"[FAILED] response not received within 1sec{response.text}"
    print(f"[PASSED][GET] Challenge2")
    #challenge2
    response_two=requests.get(f"{BASE_URL}/posts?userId=999")
    assert response_two.json()==[],f"[FAILED] the received status code is{response_two.status_code}"
    print(f"[PASSED][GET] challenge3: ")


if __name__ == "__main__":
    test_get()
    test_post()
    test_put()
    test_delete()
    test_all_get()