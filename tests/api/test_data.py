from faker import Faker

faker = Faker("ru_RU")


def generate_user_data_for_register_and_auth():
    login = faker.user_name()
    return {
        "login": login,
        "email": f"{login}@mail.ru",
        "password": login
    }

def generate_data_about_user():
    name = faker.name()
    location = faker.city()
    icq = faker.text(max_nb_chars=15)
    skype = faker.text(max_nb_chars=15)
    info = faker.text(max_nb_chars=15)
    profile_picture_url = faker.url()
    medium_profile_picture_url = faker.url()
    small_profile_picture_url = faker.url()
    return {
        "name": name,
        "location": location,
        "icq": icq,
        "skype": skype,
        "info": info,
        "profile_picture_url": profile_picture_url,
        "medium_profile_picture_url": medium_profile_picture_url,
        "small_profile_picture_url": small_profile_picture_url
    }