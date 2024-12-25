from faker import Faker

faker = Faker("ru_RU")


def generate_user_data():
    login = faker.user_name()
    return {
        "login": login,
        "email": f"{login}@mail.ru",
        "password": login
    }
