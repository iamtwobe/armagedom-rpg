import requests
import json

class AdminAPI:
    def __init__(self, host="http://127.0.0.1:8080", token=""):
        self.base_url = host + "/admin"
        self.headers = {"X-API-Key": token, "Content-Type": "application/json"}

    def send(self, endpoint, data=None):
        url = f"{self.base_url}/{endpoint}"
        r = requests.post(url, headers=self.headers, data=json.dumps(data or {}))
        return r.json()
