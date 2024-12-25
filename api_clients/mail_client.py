import json
from api_clients.base_client import BaseClient
import requests


class MailClient(BaseClient):
    def find_letter_by_login(self, login):
        # Отправляю запрос в Mail API, используя логин пользователя, созданного в предыдущем тесте
        endpoint = f"mail/search?query={login}"
        path = self.base_url + endpoint
        self.log_request(method="GET", endpoint=endpoint)
        response_from_mail = requests.request("GET", url=path, headers=self.headers)
        self.log_response(response_from_mail)

        # Перевожу ответ в JSON, используя ключи и индексы добираюсь до строки, которую нужно преобразовать в dict,
        # используя метод loads модуля json; затем в словаре нахожу по ключу ссылку и её спличу по слэшу,
        # чтобы получить токен
        token = json.loads(response_from_mail.json()["items"][0]["Content"]["Body"])["ConfirmationLinkUrl"].split("/")[
            -1]
        return token
