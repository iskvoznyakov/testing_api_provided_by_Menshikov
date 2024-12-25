from api_clients.base_client import BaseClient
import requests


class RegisterClient(BaseClient):
    def register_user(self, payload):
        endpoint = "user/register"
        path = self.base_url + endpoint
        self.log_request(method="POST", endpoint=endpoint, payload=payload)
        response = requests.request(method="POST", url=path, headers=self.headers, json=payload)
        self.log_response(response)
        return response

    def activate_user(self, token):
        # Вставляю полученный из письма токен в запрос для активации пользователя
        endpoint = f"user/activate?token={token}"
        path = self.base_url + endpoint
        self.log_request(method="PUT", endpoint=endpoint)
        response = requests.request("PUT", url=path, headers=self.headers)
        self.log_response(response)
        return response
