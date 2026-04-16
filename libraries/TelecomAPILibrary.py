import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
import time
import json
from robot.api.deco import keyword
from api_practice.oauth import OAuth


class TelecomAPILibrary:
    """
    RF Custom Library for Telecom Subscriber API
    Wraps all subscriber lifecycle operations as RF Keywords
    """
    ROBOT_LIBRARY_SCOPE = 'SUITE'

    def __init__(self):
        self.oauth_token  = None
        self.base_url     = None
        self.new_sub_id   = None   # created subscriber id
        self.suspended_id = None   # suspended subscriber id

    # ── Setup ──────────────────────────────────────────────
    @keyword("Setup API Session")
    def setup_api_session(self, base_url, client_id, client_secret):
        self.base_url = base_url
        oauth = OAuth(
            client_id=client_id,
            client_secret=client_secret,
            base_url=base_url
        )
        self.oauth_token = oauth.get_header()

    # ── Helper ─────────────────────────────────────────────
    def _search_json(self, payload, item_to_search: str) -> list:
        result = []
        if isinstance(payload, dict):
            if item_to_search in payload:
                result.append(payload[item_to_search])
            for value in payload.values():
                result.extend(self._search_json(value, item_to_search))
        elif isinstance(payload, list):
            for item in payload:
                result.extend(self._search_json(item, item_to_search))
        return result

    # --search json--
    @keyword("Extract Field From Response")
    def extract_field_from_response(self, payload,item_to_search) -> list:
        return self._search_json(payload, item_to_search)

    # ── Subscriber Keywords ────────────────────────────────
    @keyword("Get All Subscribers")
    def get_all_subscribers(self):
        response = requests.get(
            url=f"{self.base_url}/api/subscribers",
            headers=self.oauth_token
        )
        assert response.status_code == 200, \
            f"Expected 200 got {response.status_code}: {response.text}"
        return response.json()

    @keyword("Create Subscriber")
    def create_subscriber(self, name: str):
        phone = str(int(time.time() * 1000))[-10:]
        payload = {
            "name":  name,
            "phone": phone,
            "email": "test@telecom.com",
            "plan":  "premium"
        }
        response = requests.post(
            url=f"{self.base_url}/api/subscribers",
            json=payload,
            headers=self.oauth_token
        )
        assert response.status_code == 201, \
            f"Expected 201 got {response.status_code}: {response.text}"
        self.new_sub_id = response.json()["id"]
        return self.new_sub_id

    @keyword("Get Subscriber By ID")
    def get_subscriber_by_id(self, sub_id: str):
        response = requests.get(
            url=f"{self.base_url}/api/subscribers/{sub_id}",
            headers=self.oauth_token
        )
        assert response.status_code == 200, \
            f"Expected 200 got {response.status_code}: {response.text}"
        return response.json()

    @keyword("Update Subscriber")
    def update_subscriber(self, sub_id: str, name: str, email: str, plan: str):
        payload = {"name": name, "email": email, "plan": plan}
        response = requests.put(
            url=f"{self.base_url}/api/subscribers/{sub_id}",
            json=payload,
            headers=self.oauth_token
        )
        assert response.status_code == 200, \
            f"Expected 200 got {response.status_code}: {response.text}"
        return response.json()

    @keyword("Suspend Subscriber")
    def suspend_subscriber(self, sub_id: str):
        response = requests.put(
            url=f"{self.base_url}/api/subscribers/{sub_id}/suspend",
            headers=self.oauth_token
        )
        assert response.status_code == 200, \
            f"Expected 200 got {response.status_code}: {response.text}"
        self.suspended_id = sub_id
        return sub_id

    @keyword("Activate Subscriber")
    def activate_subscriber(self, sub_id: str):
        response = requests.put(
            url=f"{self.base_url}/api/subscribers/{sub_id}/activate",
            headers=self.oauth_token
        )
        assert response.status_code == 200, \
            f"Expected 200 got {response.status_code}: {response.text}"
        return sub_id

    @keyword("Get Subscriber Usage")
    def get_subscriber_usage(self, sub_id: str):
        response = requests.get(
            url=f"{self.base_url}/api/subscribers/{sub_id}/usage",
            headers=self.oauth_token
        )
        assert response.status_code == 200, \
            f"Expected 200 got {response.status_code}: {response.text}"
        return response.json()

    @keyword("Delete Subscriber")
    def delete_subscriber(self, sub_id: str):
        response = requests.delete(
            url=f"{self.base_url}/api/subscribers/{sub_id}",
            headers=self.oauth_token
        )
        assert response.status_code == 200, \
            f"Expected 200 got {response.status_code}: {response.text}"

    # ── Negative Tests ─────────────────────────────────────
    @keyword("Get Subscriber Without Token Should Fail")
    def get_without_token(self):
        response = requests.get(
            url=f"{self.base_url}/api/subscribers"
        )
        assert response.status_code == 401, \
            f"Expected 401 got {response.status_code}"

    @keyword("Get Non Existent Subscriber Should Fail")
    def get_non_existent(self, sub_id: str = "INVALID999"):
        response = requests.get(
            url=f"{self.base_url}/api/subscribers/{sub_id}",
            headers=self.oauth_token
        )
        assert response.status_code == 404, \
            f"Expected 404 got {response.status_code}"

    @keyword("Create Duplicate Subscriber Should Fail")
    def create_duplicate(self, phone: str = "9876543210"):
        payload = {
            "name": "Duplicate", "phone": phone,
            "email": "dup@test.com", "plan": "basic"
        }
        response = requests.post(
            url=f"{self.base_url}/api/subscribers",
            json=payload,
            headers=self.oauth_token
        )
        assert response.status_code == 409, \
            f"Expected 409 got {response.status_code}"

    @keyword("Create Subscriber With Missing Fields Should Fail")
    def create_missing_fields(self):
        payload = {"name": "Incomplete"}
        response = requests.post(
            url=f"{self.base_url}/api/subscribers",
            json=payload,
            headers=self.oauth_token
        )
        assert response.status_code == 400, \
            f"Expected 400 got {response.status_code}"
        assert "missing" in response.json()

    @keyword("Suspend Already Suspended Should Fail")
    def suspend_already_suspended(self, sub_id: str):
        # First suspend
        requests.put(
            url=f"{self.base_url}/api/subscribers/{sub_id}/suspend",
            headers=self.oauth_token
        )
        # Second suspend — should fail
        response = requests.put(
            url=f"{self.base_url}/api/subscribers/{sub_id}/suspend",
            headers=self.oauth_token
        )
        assert response.status_code == 409, \
            f"Expected 409 got {response.status_code}"
        # Cleanup
        requests.put(
            url=f"{self.base_url}/api/subscribers/{sub_id}/activate",
            headers=self.oauth_token
        )