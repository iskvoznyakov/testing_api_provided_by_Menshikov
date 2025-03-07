import allure


@allure.title("Позитивная авторизация нового пользователя")
@allure.description("Проверяем авторизацию пользователя через API")
def test_valid_auth_user(log_test, register_client, mail_client, auth_client, user_data):
    with allure.step("Отправляем запрос на регистрацию"):
        response = register_client.register_user(user_data)
        assert response.status_code == 201, f"Registration failed, status_code of the response: {response.status_code}"
    with allure.step("Получаем токен активации и активируем пользователя"):
        token = mail_client.find_letter_by_login(user_data["login"])
        response = register_client.activate_user(token)
        assert response.json()["resource"]["login"] == user_data["login"], "Activation of user failed"
    with allure.step("Пытаемся авторизоваться только что созданным и активированным пользователем"):
        payload = {
            "login": user_data["login"],
            "password": user_data["password"],
            "rememberMe": True
        }
        response = auth_client.auth_user(payload)
    with allure.step("Проверяем статус-код и сообщение о валидации в ответе"):
        assert response.status_code == 200, f"Authorization failed, status_code of the response: {response.status_code}"
        assert "token" in response.json()["metadata"], "There's no any token"


@allure.title("Негативная авторизация нового пользователя")
@allure.description("Проверяем некорректную авторизацию пользователя через API (некорректный пароль)")
def test_invalid_auth_user(log_test, register_client, mail_client, auth_client, user_data):
    with allure.step("Отправляем запрос на регистрацию"):
        response = register_client.register_user(user_data)
        assert response.status_code == 201, f"Registration failed, status_code of the response: {response.status_code}"
    with allure.step("Получаем токен активации и активируем пользователя"):
        token = mail_client.find_letter_by_login(user_data["login"])
        response = register_client.activate_user(token)
        assert response.json()["resource"]["login"] == user_data["login"], "Activation of user failed"
    with allure.step(
            "Пытаемся авторизоваться только что созданным и активированным пользователем, используя неправильный пароль"):
        payload = {
            "login": user_data["login"],
            "password": "password!1!",
            "rememberMe": True
        }
        response = auth_client.auth_user(payload)
        assert response.status_code == 400, f"Authorization didn't fail, status_code of the response: {response.status_code}"
        assert response.json()["detail"]["errors"]["login"][
                   0] == "The password is incorrect. Did you forget to switch the keyboard?", "Authorization didn't fail"
