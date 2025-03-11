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

    def reset_password(self, login, email):
        payload = {
            "login": login,
            "email": email
        }
        return self._request(method="POST", endpoint="account/reset-password", json=payload)

    def change_password(self, login, token, old_password, new_password):
        payload = {
            "login": login,
            "token": token,
            "oldPassword": old_password,
            "newPassword": new_password
        }
        return self._request(method="PUT", endpoint="account/change-password", json=payload)
