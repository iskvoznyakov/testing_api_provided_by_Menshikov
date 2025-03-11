import json

from api_clients.base_client import BaseClient


class MailClient(BaseClient):
    def find_activate_letter_by_login(self, login):
        # Отправляю запрос в Mail API, используя логин пользователя, зарегистрированного пользователя
        response_from_mail = self._request(method="GET", endpoint=f"mail/search?query={login}")

        # Перевожу ответ в JSON, используя ключи и индексы добираюсь до строки, которую нужно преобразовать в dict,
        # используя метод loads модуля json; затем в словаре нахожу по ключу ссылку и её спличу по слэшу,
        # чтобы получить токен
        bodies_of_found_items = response_from_mail.json()["items"]
        if response_from_mail.json()["total"] == 1:
            token = \
                json.loads(bodies_of_found_items[0]["Content"]["Body"])["ConfirmationLinkUrl"].split("/")[
                    -1]
        else:
            for body in bodies_of_found_items:
                if "ConfirmationLinkUrl" in json.loads(body["Content"]["Body"]):
                    token = \
                        json.loads(body["Content"]["Body"])["ConfirmationLinkUrl"].split("/")[
                            -1]
        return token

    def find_reset_password_letter_by_login(self, login):
        # Отправляю запрос в Mail API, используя логин пользователя, зарегистрированного пользователя
        response_from_mail = self._request(method="GET", endpoint=f"mail/search?query={login}")

        # Перевожу ответ в JSON, используя ключи и индексы добираюсь до строки, которую нужно преобразовать в dict,
        # используя метод loads модуля json; затем в словаре нахожу по ключу ссылку и её спличу по слэшу,
        # чтобы получить токен
        bodies_of_found_items = response_from_mail.json()["items"]
        for body in bodies_of_found_items:
            if "ConfirmationLinkUri" in json.loads(body["Content"]["Body"]):
                token = \
                            json.loads(body["Content"]["Body"])["ConfirmationLinkUri"].split("/")[
                                -1]
        return token

    def find_delete_user_letter_by_login(self, login):
        # Отправляю запрос в Mail API, используя логин пользователя, зарегистрированного пользователя
        response_from_mail = self._request(method="GET", endpoint=f"mail/search?query={login}")

        # Перевожу ответ в JSON, используя ключи и индексы добираюсь до строки, которую нужно преобразовать в dict,
        # используя метод loads модуля json; затем в словаре нахожу по ключу ссылку и её спличу по слэшу,
        # чтобы получить токен
        bodies_of_found_items = response_from_mail.json()["items"]
        for body in bodies_of_found_items:
            if "Token for delete your account:" in body["Content"]["Body"]:
                token = body["Content"]["Body"].split("Token for delete your account: ")[-1].split(',')[0]
            return token