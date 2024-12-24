import json
from utils.logger import setup_logger

import requests

# Настроим логгер для класса ApiClient
logger = setup_logger('ApiClient')


class ApiClient:
    def __init__(self, host, headers=None):
        self.host = host
        self.headers = headers or {
            'accept': '*/*',
            'Content-Type': 'application/json'
        }

    def log_request(self, method, endpoint, **kwargs):
        """
        Логирует информацию о запросе.
        :param method: HTTP метод (get, post, put, delete)
        :param endpoint: Конечная точка URL
        :param kwargs: Дополнительные параметры запроса (например, params, json)
        """
        logger.info(f"Request {method.upper()} {self.host}{endpoint} with params {kwargs}")

    def log_response(self, response):
        """
        Логирует информацию об ответе.
        :param response: Ответ, полученный от API
        """
        logger.info(
            f"Response: {response.status_code} - {response.text}...")  # Логируем статус-код и все символы ответа

    def register_user(self, payload):
        endpoint = "register/user/register"
        path = self.host + endpoint
        self.log_request(method="POST", endpoint=endpoint, payload=payload)
        response = requests.request(method="POST", url=path, headers=self.headers, json=payload)
        self.log_response(response)
        return response

    def activate_user(self, login):
        # Отправляю запрос в Mail API, используя логин пользователя, созданного в предыдущем тесте
        endpoint = f"/mail/mail/search?query={login}"
        path = self.host + endpoint
        self.log_request(method="GET", endpoint=endpoint)
        response_from_mail = requests.request("GET", url=path, headers=self.headers)
        self.log_response(response_from_mail)

        # Перевожу ответ в JSON, используя ключи и индексы добираюсь до строки, которую нужно преобразовать в dict,
        # используя метод loads модуля json; затем в словаре нахожу по ключу ссылку и её спличу по слэшу,
        # чтобы получить токен
        token = json.loads(response_from_mail.json()["items"][0]["Content"]["Body"])["ConfirmationLinkUrl"].split("/")[
            -1]

        # Вставляю полученный токен в запрос для активации пользователя
        endpoint = f"register/user/activate?token={token}"
        path = self.host + endpoint
        self.log_request(method="PUT", endpoint=endpoint)
        response = requests.request("PUT", url=path, headers=self.headers)
        self.log_response(response)
        return response
