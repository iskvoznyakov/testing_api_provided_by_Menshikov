# Позитивная проверка авторизации активированного пользователя
def test_valid_auth_user(log_test, register_client, mail_client, auth_client, user_data):
    response = register_client.register_user(user_data)
    assert response.status_code == 201, f"Registration failed, status_code of the response: {response.status_code}"

    token = mail_client.find_letter_by_login(user_data["login"])
    response = register_client.activate_user(token)
    assert response.json()["resource"]["login"] == user_data["login"], "Activation of user failed"

    payload = {
        "login": user_data["login"],
        "password": user_data["password"],
        "rememberMe": True
    }
    response = auth_client.auth_user(payload)
    assert response.status_code == 200, f"Authorization failed, status_code of the response: {response.status_code}"
    assert "token" in response.json()["metadata"], "There's no any token"


# Пока что подряд эти тесты запускать не получится, т.к. они используют одинаковые перс. данные
# Негативная проверка авторизации активированного пользователя (некорректный пароль)
def test_invalid_auth_user(log_test, register_client, mail_client, auth_client, user_data):
    response = register_client.register_user(user_data)
    assert response.status_code == 201, f"Registration failed, status_code of the response: {response.status_code}"

    token = mail_client.find_letter_by_login(user_data["login"])
    response = register_client.activate_user(token)
    assert response.json()["resource"]["login"] == user_data["login"], "Activation of user failed"

    payload = {
        "login": user_data["login"],
        "password": "password!1!",
        "rememberMe": True
    }
    response = auth_client.auth_user(payload)
    assert response.status_code == 400, f"Authorization didn't fail, status_code of the response: {response.status_code}"
    assert response.json()["detail"]["errors"]["login"][
               0] == "The password is incorrect. Did you forget to switch the keyboard?", "Authorization didn't fail"
