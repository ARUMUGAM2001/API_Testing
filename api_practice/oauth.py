import requests

class OAuth:
    def __init__(self,client_id,client_secret,base_url,scope=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url
        self.scope = scope
        self.oauth_token=None

    def get_access_token(self):
        self.base_url=f"{self.base_url}/oauth/token"
        payload={
            "client_id":self.client_id,
            "client_secret":self.client_secret,
            "grant_type":"client_credentials"
        }
        if self.scope:
            payload["scope"]=self.scope
        response=requests.post(self.base_url,data=payload)
        if response.status_code==200:
            self.oauth_token=response.json()["access_token"]
        else:
            raise Exception(response.text)

    def get_header(self):
        if not self.oauth_token:
            self.get_access_token()
        return {"Authorization":f"Bearer {self.oauth_token}"}
