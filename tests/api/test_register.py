import allure
import pytest


@allure.title("Позитивная регистрация нового пользователя")
@allure.description("Проверяем регистрацию пользователя через API")
def test_valid_register_user(log_test, register_client, reg_auth_data):
    # В payload вставляю логин, который был заранее сгенерирован с помощью fakera
    with allure.step("Отправляем запрос на регистрацию"):
        response = register_client.register_user(reg_auth_data)
    with allure.step("Проверяем статус-код и сообщение ответа"):
        assert response.status_code == 201, f"Registration failed, status_code of the response: {response.status_code}"
        assert response.json()[
                   "message"] == "User has been registered and expects confirmation by e-mail", "Registration failed"


@allure.title("Негативная регистрация нового пользователя")
@allure.description("Проверяем валидацию при регистрации пользователя через API")
# Негативная проверка регистрации пользователя
# В параметризации - последний тест падает из-за бага, соответственно его пометил xfailом, также добавил ids
@pytest.mark.parametrize("login, email, password, response_field, validation_message",
                         [('', "emmaail@mail.ru", "password", "Login", "Empty"),
                          ("llooggiinnn", "", "password", "Email", "Empty"),
                          ("llooggiinnn", "emmaail@mail.ru", "", "Password", "Empty"),
                          ('l', "emmaail@mail.ru", "password", "Login", "Short"),
                          ("llooggiinnn", "emmaail@mail.ru", "12345", "Password", "Short"),
                          ('l' * 61, "emmaail@mail.ru", "password", "Login", "Long"),
                          ("llooggiinnn", "email.ru", "password", "Email", "Invalid"),
                          pytest.param("llooggiinnnn", "emailll@mailru", "password", "Email", "Invalid",
                                       marks=pytest.mark.xfail(reason="bug"))],
                         ids=["empty login", "empty email", "empty password", "short login", "short password",
                              "long login", "email without @", "email without . in domain part"])
def test_invalid_register_user(log_test, register_client, login, email, password, response_field, validation_message):
    # В payload вставляю логин, который был заранее сгенерирован с помощью fakera
    payload = {
        "login": login,
        "email": email,
        "password": password
    }
    with allure.step("Отправляем запрос на регистрацию"):
        response = register_client.register_user(payload)
    with allure.step("Проверяем статус-код и сообщение о валидации в ответе"):
        assert response.status_code == 400, f"Registration succeed, status_code of the response: {response.status_code}"
        assert validation_message in response.json()["detail"]["errors"][response_field], "Registration succeed"


@allure.title("Позитивная активация зарегистрированного пользователя")
@allure.description("Проверяем активации зарегистрированного пользователя через API")
# Позитивная проверка активации пользователя, созданного в предыдущем тесте
def test_valid_activate_user(log_test, register_client, mail_client, reg_auth_data):
    with allure.step("Отправляем запрос на регистрацию"):
        response = register_client.register_user(reg_auth_data)
    with allure.step("Активируем пользователя с помощью полученного токена"):
        # Использую логин пользователя, созданного в предыдущем тесте
        token = mail_client.find_activate_letter_by_login(reg_auth_data["login"])
        response = register_client.activate_user(token)
    with allure.step("Проверяем статус-код и сообщение о валидации в ответе"):
        assert response.status_code == 200, f"Activation failed, status_code of the response: {response.status_code}"
        assert response.json()["resource"]["login"] == reg_auth_data["login"], "Activation of user failed"
