import requests

from utils.logger import setup_logger


class BaseClient:
    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.headers = headers or {
            'accept': '*/*',
            'Content-Type': 'application/json'
        }
        self.logger = setup_logger(self.__class__.__name__)

    def log_request(self, method, endpoint, **kwargs):
        """
        Логирует информацию о запросе.
        :param method: HTTP метод (get, post, put, delete)
        :param endpoint: Конечная точка URL
        :param kwargs: Дополнительные параметры запроса (например, params, json)
        """
        self.logger.info(f"Request {method.upper()} {self.base_url}{endpoint} with params {kwargs}")

    def log_response(self, response):
        """
        Логирует информацию об ответе.
        :param response: Ответ, полученный от API
        """
        self.logger.info(
            f"Response: {response.status_code} - {response.text}...")  # Логируем статус-код и все символы ответа

    def _request(self, method, endpoint, **kwargs):
        """Общий метод для отправки запросов"""
        url = f"{self.base_url}{endpoint}"
        self.log_request(method, endpoint, **kwargs)
        response = requests.request(method, url, headers=self.headers, **kwargs)
        self.log_response(response)
        return response
