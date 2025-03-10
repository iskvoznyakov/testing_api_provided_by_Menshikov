from api_clients.base_client import BaseClient


class AccountClient(BaseClient):
    def __init__(self, base_url, headers=None):
        super().__init__(base_url, headers)
        self.mapping_list = {"profile_picture_url": "originalPictureUrl",
                             "small_profile_picture_url": "smallPictureUrl",
                             "medium_profile_picture_url": "mediumPictureUrl"}

    def get_account_info(self, auth_token):
        self.headers.update({"token": auth_token})
        return self._request(method="GET", endpoint="account/info")

    def change_account_info(self, auth_token, payload):
        self.headers.update({"token": auth_token})
        return self._request(method="PATCH", endpoint="account/info", json=payload)
