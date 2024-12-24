from faker import Faker

faker = Faker("ru_RU")
login = faker.user_name()


# Позитивная проверка регистрации пользователя
def test_register_user(log_test, client):
    # В payload вставляю логин, который был заранее сгенерирован с помощью fakera
    payload = {
        "login": login,
        "email": f"{login}@mail.ru",
        "password": login
    }
    response = client.register_user(payload)
    assert response.status_code == 201, f"Registration failed, status_code of the response: {response.status_code}"
    assert response.json()[
               "message"] == "User has been registered and expects confirmation by e-mail", "Registration failed"


# Позитивная проверка активации пользователя, созданного в предыдущем тесте
def test_activate_user(log_test, client):
    # Использую логин пользователя, созданного в предыдущем тесте
    response = client.activate_user(login=login)
    assert response.status_code == 200, f"Activation failed, status_code of the response: {response.status_code}"
    assert response.json()["resource"]["login"] == login, "Activation of user failed"
