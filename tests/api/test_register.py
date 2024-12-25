# Позитивная проверка регистрации пользователя
def test_register_user(log_test, register_client, user_data):
    # В payload вставляю логин, который был заранее сгенерирован с помощью fakera
    response = register_client.register_user(user_data)
    assert response.status_code == 201, f"Registration failed, status_code of the response: {response.status_code}"
    assert response.json()[
               "message"] == "User has been registered and expects confirmation by e-mail", "Registration failed"


# Позитивная проверка активации пользователя, созданного в предыдущем тесте
def test_activate_user(log_test, register_client, mail_client, user_data):
    token = mail_client.find_letter_by_login(user_data["login"])
    # Использую логин пользователя, созданного в предыдущем тесте
    response = register_client.activate_user(token)
    assert response.status_code == 200, f"Activation failed, status_code of the response: {response.status_code}"
    assert response.json()["resource"]["login"] == user_data["login"], "Activation of user failed"
