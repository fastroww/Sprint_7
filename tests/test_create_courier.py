import pytest
import allure
import requests
from constants import COURIER_URL
from testdata.courier_data import generate_courier_data
from conftest import assert_status_code


def _create_courier_payload(courier_data):
    """Создаёт payload для создания курьера"""
    return {
        "login": courier_data.login,
        "password": courier_data.password,
        "firstName": courier_data.firstName
    }


@allure.suite("Courier API")
@allure.sub_suite("Create courier")
class TestCreateCourier:

    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self, courier_fixture):
        """
        1. Используем фикстуру для создания курьера
        2. Проверяем статус код 200 при логине и наличие ключа "ok": true
        """
        courier = courier_fixture
        login_response = requests.post(f"{COURIER_URL}/login", json={
            "login": courier["data"].login,
            "password": courier["data"].password
        })
        assert_status_code(login_response, 200, "Курьер не залогинился")
        courier_id = login_response.json().get("id")
        assert courier_id, "В ответе на логин не вернули id!"

    @allure.title("Нельзя создать двух одинаковых курьеров (дубликаты)")
    def test_create_courier_duplicate(self, courier_fixture):
        """
        1. Используем фикстуру для создания курьера.
        2. Создаём такого же курьера второй раз (дубликат).
        3. Проверяем 409.
        """
        courier = courier_fixture
        payload = _create_courier_payload(courier["data"])

        # Второй запрос - дубликат
        response_2 = requests.post(COURIER_URL, json=payload)
        assert_status_code(response_2, 409, "Ожидался 409 при создании дубликата")
        assert "message" in response_2.json(), "Отсутствует сообщение об ошибке"

    @allure.title("Создание курьера без пароля (ожидаем 400)")
    def test_create_courier_without_password(self):
        """
        Негативный тест, когда поле password не передаём.
        Здесь курьера в итоге НЕ создаём (ожидается 400),
        """
        courier_data = generate_courier_data()
        payload = _create_courier_payload(courier_data)
        payload.pop("password")

        response = requests.post(COURIER_URL, json=payload)
        assert_status_code(response, 400, "Ожидался 400 при отсутствии пароля")
        error_message = response.json().get("message")
        assert error_message == "Недостаточно данных для создания учетной записи", (
            f"Ожидали сообщение 'Недостаточно данных для создания учетной записи', "
            f"но получили: {error_message}"
        )

    @allure.title("Ошибка, если логин уже существует (другая проверка дубликатов)")
    def test_create_courier_existing_login(self, courier_fixture):
        """
        1. Используем фикстуру для создания курьера.
        2. Создаём второго курьера с тем же логином.
        3. Ожидаем ошибку 409.
        """
        # Первый курьер
        courier = courier_fixture
        payload_2 = {
            "login": courier["data"].login,
            "password": "password_2",
            "firstName": "SecondCourier"
        }
        response_2 = requests.post(COURIER_URL, json=payload_2)
        assert_status_code(response_2, 409, f"Expected 409, got {response_2.status_code}")
        assert "message" in response_2.json(), "No error message in response"


