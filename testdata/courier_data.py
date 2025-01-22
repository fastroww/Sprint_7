from dataclasses import dataclass
import random
import string

DEFAULT_STRING_LENGTH = 10  # Константа для длины строки
ALLOWED_CHARACTERS = string.ascii_lowercase # Константа для набора символов


def generate_random_string(length=DEFAULT_STRING_LENGTH, allowed_chars=ALLOWED_CHARACTERS) -> str:
    """Генерирует случайную строку из символов."""
    return ''.join(random.choice(allowed_chars) for _ in range(length))

@dataclass
class CourierData:
    """Класс, описывающий поля для курьера."""
    login: str
    password: str
    firstName: str

def generate_courier_data() -> CourierData:
    """
    Генерирует валидные данные курьера
    (логин, пароль, имя) со случайными значениями.
    """
    return CourierData(
        login=generate_random_string(),
        password=generate_random_string(),
        firstName=generate_random_string()
    )