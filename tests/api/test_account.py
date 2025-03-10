import allure


@allure.title("Позитивная проверка получения информации о пользователе")
@allure.description("Проверяем получение информации о пользователе через API")
def test_valid_get_info_about_user(log_test, register_client, mail_client, auth_client, account_client, user_data):
    with allure.step("Предусловие: регистрация и активация пользователя"):
        # Регистрация
        response = register_client.register_user(user_data)
        assert response.status_code == 201, f"Registration failed, status_code of the response: {response.status_code}"
        # Получаем токен активации и активируем пользователя
        token = mail_client.find_letter_by_login(user_data["login"])
        response = register_client.activate_user(token)
        assert response.json()["resource"]["login"] == user_data["login"], "Activation of user failed"
        # Пытаемся авторизоваться только что созданным и активированным пользователем
        payload = {
            "login": user_data["login"],
            "password": user_data["password"],
            "rememberMe": True
        }
        response = auth_client.auth_user(payload)
        assert response.status_code == 200, f"Authorization failed, status_code of the response: {response.status_code}"
        assert "token" in response.json()["metadata"], "There's no any token"
        # Забираем токен из ответа
        auth_token = response.json()["metadata"]["token"]
    with allure.step("Получаем информацию о пользователе"):
        response = account_client.get_account_info(auth_token=auth_token)
        assert response.status_code == 200, f"Getting info failed, status_code of the response: {response.status_code}"
        assert user_data["login"] == response.json()["resource"]["login"]


@allure.title("Негативная проверка получения информации о пользователе")
@allure.description("Проверяем получение информации о пользователе через API")
def test_invalid_get_info_about_user(log_test, register_client, mail_client, auth_client, account_client, user_data):
    with allure.step("Предусловие: регистрация и активация пользователя"):
        # Регистрация
        response = register_client.register_user(user_data)
        assert response.status_code == 201, f"Registration failed, status_code of the response: {response.status_code}"
        # Получаем токен активации и активируем пользователя
        token = mail_client.find_letter_by_login(user_data["login"])
        response = register_client.activate_user(token)
        assert response.json()["resource"]["login"] == user_data["login"], "Activation of user failed"
        # Пытаемся авторизоваться только что созданным и активированным пользователем
        payload = {
            "login": user_data["login"],
            "password": user_data["password"],
            "rememberMe": True
        }
        response = auth_client.auth_user(payload)
        assert response.status_code == 200, f"Authorization failed, status_code of the response: {response.status_code}"
        assert "token" in response.json()["metadata"], "There's no any token"
        # Забираем токен из ответа
        auth_token = response.json()["metadata"]["token"]
    with allure.step("Получаем информацию о пользователе с некорректным токеном авторизации"):
        response = account_client.get_account_info(auth_token=auth_token + "1")
        assert response.status_code == 400, f"Getting info not failed, status_code of response: {response.status_code}"
        assert response.json()["detail"]["status"] == 401, f"Status of response not 401, but {response.status_code}"
        assert response.json()["detail"]["title"] == "User must be authenticated", f"Authentication not failed"
