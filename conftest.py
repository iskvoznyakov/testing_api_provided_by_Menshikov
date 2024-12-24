import pytest
from api import ApiClient
from config.config import BASE_HOST
from utils.logger import setup_logger

# Настройка логгера для тестов
logger = setup_logger('TestApi')


@pytest.fixture(scope="function")
def log_test(request):
    """
    Фикстура для логирования начала и конца каждого теста.
    :param request: Объект запроса, который предоставляет информацию о текущем тесте
    """

    logger.info(f"Starting test: {request.node.name}")  # Логируем начало теста
    yield  # Делаем паузу до завершения теста
    logger.info(f"Finished test: {request.node.name}")  # Логируем окончание теста


@pytest.fixture()
def client():
    return ApiClient(BASE_HOST)
