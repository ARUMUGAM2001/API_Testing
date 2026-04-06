import requests

BASE_URL="https://jsonplaceholder.typicode.com"
response=requests.get(f"{BASE_URL}/posts/1")
print("[Status_Code]",response.status_code)
print("[Response JSON]",response.json())
print("[Title]",response.json()["title"])

#status code validation
assert response.status_code == 200
print("[Status_Code]",response.status_code)

#response time
assert response.elapsed.total_seconds() < 2.0

#key validation
assert "title" in response.json()
print("[Title]",response.json()["title"])

#value validation
assert response.json()["id"]==1

# 5. Content type
assert response.headers["Content-Type"] == "application/json; charset=utf-8"

print(f"[Headers]: {response.headers}")
