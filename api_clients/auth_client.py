from api_clients.base_client import BaseClient


class AuthClient(BaseClient):
    def auth_user(self, payload):
        return self._request(method="POST", endpoint="auth/auth", json=payload)
