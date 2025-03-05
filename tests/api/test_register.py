import allure
import pytest


@allure.title("Позитивная регистрация нового пользователя")
@allure.description("Проверяем регистрацию пользователя через API")
# Позитивная проверка регистрации пользователя
def test_valid_register_user(log_test, register_client, user_data):
    # В payload вставляю логин, который был заранее сгенерирован с помощью fakera
    with allure.step("Отправляем запрос на регистрацию"):
        response = register_client.register_user(user_data)
    with allure.step("Проверяем статус-код и сообщение ответа"):
        assert response.status_code == 201, f"Registration failed, status_code of the response: {response.status_code}"
        assert response.json()[
                   "message"] == "User has been registered and expects confirmation by e-mail", "Registration failed"


@allure.title("Негативная регистрация нового пользователя")
@allure.description("Проверяем валидацию при регистрации пользователя через API")
# Негативная проверка регистрации пользователя
@pytest.mark.parametrize("login, email, password, response_field, validation_message",
                         [('', "emmaail@mail.ru", "password", "Login", "Empty"),
                          ("llooggiinnn", "", "password", "Email", "Empty"),
                          ("llooggiinnn", "emmaail@mail.ru", "", "Password", "Empty"),
                          ('l', "emmaail@mail.ru", "password", "Login", "Short"),
                          ("llooggiinnn", "emmaail@mail.ru", "12345", "Password", "Short"),
                          ('l' * 61, "emmaail@mail.ru", "password", "Login", "Long"),
                          ("llooggiinnn", "email.ru", "password", "Email", "Invalid"),
                          pytest.param("llooggiinnn", "emaill@mailru", "password", "Email", "Invalid",
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


# Позитивная проверка активации пользователя, созданного в предыдущем тесте
def test_activate_user(log_test, register_client, mail_client, user_data):
    token = mail_client.find_letter_by_login(user_data["login"])
    # Использую логин пользователя, созданного в предыдущем тесте
    response = register_client.activate_user(token)
    assert response.status_code == 200, f"Activation failed, status_code of the response: {response.status_code}"
    assert response.json()["resource"]["login"] == user_data["login"], "Activation of user failed"
