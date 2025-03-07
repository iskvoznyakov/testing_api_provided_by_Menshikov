from api_clients.base_client import BaseClient


class RegisterClient(BaseClient):
    def register_user(self, payload):
        return self._request(method="POST", endpoint="user/register", json=payload)

    def activate_user(self, token):
        # Вставляю полученный из письма токен в запрос для активации пользователя
        return self._request(method="PUT", endpoint=f"user/activate?token={token}")
