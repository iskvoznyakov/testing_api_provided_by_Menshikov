import pytest

from api_clients.account_client import AccountClient
from api_clients.auth_client import AuthClient
from api_clients.mail_client import MailClient
from api_clients.register_client import RegisterClient
from config.config import REGISTER_API, MAIL_API, AUTH_API, ACCOUNT_API
from tests.api.test_data import generate_user_data_for_register_and_auth, generate_data_about_user
from utils.logger import setup_logger

# Настройка логгера для тестов
logger = setup_logger('TestApi')


@pytest.fixture(scope="session")
def log_test(request):
    """
    Фикстура для логирования начала и конца каждого теста.
    :param request: Объект запроса, который предоставляет информацию о текущем тесте
    """

    logger.info(f"Starting test: {request.node.name}")  # Логируем начало теста
    yield  # Делаем паузу до завершения теста
    logger.info(f"Finished test: {request.node.name}")  # Логируем окончание теста


# Генерация данных для регистрации/авторизации
@pytest.fixture(scope="function")
def reg_auth_data():
    return generate_user_data_for_register_and_auth()

# Генерация данных для пользователя
@pytest.fixture(scope="function")
def user_data():
    return generate_data_about_user()


# Клиенты
@pytest.fixture()
def register_client():
    return RegisterClient(REGISTER_API)


@pytest.fixture()
def mail_client():
    return MailClient(MAIL_API)


@pytest.fixture()
def auth_client():
    return AuthClient(AUTH_API)


@pytest.fixture()
def account_client():
    return AccountClient(ACCOUNT_API)
