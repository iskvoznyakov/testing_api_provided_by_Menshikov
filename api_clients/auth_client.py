from api_clients.base_client import BaseClient
import requests


class AuthClient(BaseClient):
    def auth_user(self, payload):
        endpoint = "auth/auth"
        path = self.base_url + endpoint
        self.log_request(method="POST", endpoint=endpoint, payload=payload)
        response = requests.request(method="POST", url=path, headers=self.headers, json=payload)
        self.log_response(response)
        return response
