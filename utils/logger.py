import logging


# Функция для настройки логгера
def setup_logger(name):
    """
    Настроить логгер для отображения логов в консоли.
    :param name: Имя логгера
    :return: Настроенный логгер
    """
    logger = logging.getLogger(name)  # Создаём логгер с заданным именем
    handler = logging.StreamHandler()  # Создаём обработчик для вывода в консоль
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # Формат логов
    handler.setFormatter(formatter)  # Устанавливаем формат логов
    logger.addHandler(handler)  # Добавляем обработчик к логгеру
    logger.setLevel(logging.INFO)  # Устанавливаем уровень логирования
    return logger  # Возвращаем настроенный логгер
