import allure
import pytest


@allure.title("Позитивная проверка получения информации о пользователе")
@allure.description("Проверяем получение информации о пользователе через API")
def test_valid_get_info_about_user(log_test, register_client, mail_client, auth_client, account_client, reg_auth_data):
    with allure.step("Предусловие: регистрация и активация пользователя"):
        # Регистрация
        response = register_client.register_user(reg_auth_data)
        assert response.status_code == 201, f"Registration failed, status_code of the response: {response.status_code}"
        # Получаем токен активации и активируем пользователя
        token = mail_client.find_activate_letter_by_login(reg_auth_data["login"])
        response = register_client.activate_user(token)
        assert response.json()["resource"]["login"] == reg_auth_data["login"], "Activation of user failed"
        # Пытаемся авторизоваться только что созданным и активированным пользователем
        payload = {
            "login": reg_auth_data["login"],
            "password": reg_auth_data["password"],
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
        assert reg_auth_data["login"] == response.json()["resource"]["login"]


@allure.title("Негативная проверка получения информации о пользователе")
@allure.description("Проверяем получение информации о пользователе через API")
def test_invalid_get_info_about_user(log_test, register_client, mail_client, auth_client, account_client,
                                     reg_auth_data):
    with allure.step("Предусловие: регистрация и активация пользователя"):
        # Регистрация
        response = register_client.register_user(reg_auth_data)
        assert response.status_code == 201, f"Registration failed, status_code of the response: {response.status_code}"
        # Получаем токен активации и активируем пользователя
        token = mail_client.find_activate_letter_by_login(reg_auth_data["login"])
        response = register_client.activate_user(token)
        assert response.json()["resource"]["login"] == reg_auth_data["login"], "Activation of user failed"
        # Пытаемся авторизоваться только что созданным и активированным пользователем
        payload = {
            "login": reg_auth_data["login"],
            "password": reg_auth_data["password"],
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


@allure.title("Позитивная проверка изменения информации о пользователе")
@allure.description("Проверяем изменение информации о пользователе через API в одном поле")
@pytest.mark.parametrize("field", ["name", "location", "icq", "skype", "info", "profile_picture_url",
                                   "medium_profile_picture_url", "small_profile_picture_url"],
                         ids=["changing name", " changing location", "changing icq",
                              "changing skype", "changing info", "changing profile_picture_url",
                              "changing medium_profile_picture_url", "changing small_profile_picture_url"])
def test_valid_change_info_about_user_in_one_field(log_test, register_client, mail_client, auth_client, account_client,
                                                   reg_auth_data, user_data, field):
    with allure.step("Предусловие: регистрация и активация пользователя"):
        # Регистрация
        response = register_client.register_user(reg_auth_data)
        assert response.status_code == 201, f"Registration failed, status_code of the response: {response.status_code}"
        # Получаем токен активации и активируем пользователя
        token = mail_client.find_activate_letter_by_login(reg_auth_data["login"])
        response = register_client.activate_user(token)
        assert response.json()["resource"]["login"] == reg_auth_data["login"], "Activation of user failed"
        # Пытаемся авторизоваться только что созданным и активированным пользователем
        payload = {
            "login": reg_auth_data["login"],
            "password": reg_auth_data["password"],
            "rememberMe": True
        }
        response = auth_client.auth_user(payload)
        assert response.status_code == 200, f"Authorization failed, status_code of the response: {response.status_code}"
        assert "token" in response.json()["metadata"], "There's no any token"
        # Забираем токен из ответа
        auth_token = response.json()["metadata"]["token"]
    with allure.step("Изменяем информацию о пользователе"):
        payload = {field: user_data[field]}
        response = account_client.change_account_info(auth_token=auth_token, payload=payload)
        assert response.status_code == 200, f"Changing info failed, status_code of the response: {response.status_code}"
        if field in account_client.mapping_list:
            assert user_data[field] == response.json()["resource"][account_client.mapping_list[field]]
        else:
            assert user_data[field] == response.json()["resource"][field]


@allure.title("Позитивная проверка изменения информации о пользователе")
@allure.description("Проверяем изменение информации о пользователе через API сразу во всех полях")
def test_valid_change_info_about_user_in_all_fields(log_test, register_client, mail_client, auth_client, account_client,
                                                    reg_auth_data, user_data):
    with allure.step("Предусловие: регистрация и активация пользователя"):
        # Регистрация
        response = register_client.register_user(reg_auth_data)
        assert response.status_code == 201, f"Registration failed, status_code of the response: {response.status_code}"
        # Получаем токен активации и активируем пользователя
        token = mail_client.find_activate_letter_by_login(reg_auth_data["login"])
        response = register_client.activate_user(token)
        assert response.json()["resource"]["login"] == reg_auth_data["login"], "Activation of user failed"
        # Пытаемся авторизоваться только что созданным и активированным пользователем
        payload = {
            "login": reg_auth_data["login"],
            "password": reg_auth_data["password"],
            "rememberMe": True
        }
        response = auth_client.auth_user(payload)
        assert response.status_code == 200, f"Authorization failed, status_code of the response: {response.status_code}"
        assert "token" in response.json()["metadata"], "There's no any token"
        # Забираем токен из ответа
        auth_token = response.json()["metadata"]["token"]
    with allure.step("Изменяем информацию о пользователе"):
        payload = user_data
        response = account_client.change_account_info(auth_token=auth_token, payload=payload)
        assert response.status_code == 200, f"Changing info failed, status_code of the response: {response.status_code}"
        for item in user_data.values():
            assert item in response.json()["resource"].values()


@allure.title("Позитивная проверка изменения пароля пользователя")
@allure.description("Проверяем изменение пароля пользователя через API")
def test_valid_change_password(log_test, register_client, mail_client, auth_client, account_client,
                               reg_auth_data, user_data):
    with allure.step("Предусловие: регистрация и активация пользователя"):
        # Регистрация
        response = register_client.register_user(reg_auth_data)
        assert response.status_code == 201, f"Registration failed, status_code of the response: {response.status_code}"
        # Получаем токен активации и активируем пользователя
        token = mail_client.find_activate_letter_by_login(reg_auth_data["login"])
        response = register_client.activate_user(token)
        assert response.json()["resource"]["login"] == reg_auth_data["login"], "Activation of user failed"
        # Пытаемся авторизоваться только что созданным и активированным пользователем
        payload = {
            "login": reg_auth_data["login"],
            "password": reg_auth_data["password"],
            "rememberMe": True
        }
        response = auth_client.auth_user(payload)
        assert response.status_code == 200, f"Authorization failed, status_code of the response: {response.status_code}"
        assert "token" in response.json()["metadata"], "There's no any token"
    with allure.step("Меняем пароль пользователю"):
        # Сбрасываем пароль, используя логин и email
        account_client.reset_password(login=reg_auth_data["login"], email=reg_auth_data["email"])
        # Находим письмо по сбросу пароля и забираем оттуда токен
        token = mail_client.find_reset_password_letter_by_login(login=reg_auth_data["login"])
        # Меняем пароль используя взятый токен
        account_client.change_password(login=reg_auth_data["login"],
                                       token=token,
                                       old_password=reg_auth_data["password"],
                                       new_password=reg_auth_data["password"] + '1')
        # Попытка авторизоваться со старым паролем
        payload = {
            "login": reg_auth_data["login"],
            "password": reg_auth_data["password"],
            "rememberMe": True
        }
        response = auth_client.auth_user(payload)
        assert response.status_code == 400
        assert response.json()["detail"]["errors"]["login"][
                   0] == "The password is incorrect. Did you forget to switch the keyboard?"

        # Попытка авторизоваться с новым паролем
        payload = {
            "login": reg_auth_data["login"],
            "password": reg_auth_data["password"] + '1',
            "rememberMe": True
        }
        response = auth_client.auth_user(payload)
        with allure.step("Проверяем статус-код и сообщение о валидации в ответе"):
            assert response.status_code == 200, f"Authorization failed, status_code of the response: {response.status_code}"
            assert "token" in response.json()["metadata"], "There's no any token"


def test_valid_delete_account(log_test, register_client, mail_client, auth_client, account_client,
                              reg_auth_data, user_data):
    with allure.step("Предусловие: регистрация и активация пользователя"):
        # Регистрация
        response = register_client.register_user(reg_auth_data)
        assert response.status_code == 201, f"Registration failed, status_code of the response: {response.status_code}"
        # Получаем токен активации и активируем пользователя
        token = mail_client.find_activate_letter_by_login(reg_auth_data["login"])
        response = register_client.activate_user(token)
        assert response.json()["resource"]["login"] == reg_auth_data["login"], "Activation of user failed"
        # Пытаемся авторизоваться только что созданным и активированным пользователем
        payload = {
            "login": reg_auth_data["login"],
            "password": reg_auth_data["password"],
            "rememberMe": True
        }
        response = auth_client.auth_user(payload)
        assert response.status_code == 200, f"Authorization failed, status_code of the response: {response.status_code}"
        assert "token" in response.json()["metadata"], "There's no any token"
        auth_token = response.json()["metadata"]["token"]
    with allure.step("Удаляем пользователя"):
        response = account_client.request_for_deleting_account(email=reg_auth_data["email"], auth_token=auth_token)
        delete_token = mail_client.find_delete_user_letter_by_login(reg_auth_data["login"])
        response = account_client.delete_account(delete_token=delete_token, auth_token=auth_token)
        assert response.status_code == 204
        # Попытка авторизоваться удаленным пользователем
        payload = {
            "login": reg_auth_data["login"],
            "password": reg_auth_data["password"],
            "rememberMe": True
        }
        response = auth_client.auth_user(payload)
    with allure.step("Проверяем статус-код и сообщение о валидации в ответе"):
        assert response.status_code == 400, f"Authorization not failed, status_code of the response: {response.status_code}"
        assert response.json()["detail"]["errors"]["login"][
                   0] == "There are no users found with this login. Maybe there was a typo?", "Authorization not failed"
