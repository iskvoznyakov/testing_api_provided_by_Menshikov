from api_clients.base_client import BaseClient


class AccountClient(BaseClient):
    def get_account_info(self, auth_token):
        self.headers.update({"token": auth_token})
        return self._request(method="GET", endpoint="account/info")
