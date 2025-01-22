import pytest
import requests
import allure
from constants import COURIER_URL
from conftest import courier_fixture, assert_status_code

def _create_login_payload(login, password):
    return {
        "login": login,
        "password": password
    }

@allure.suite("Courier API - Login")
class TestCourierLogin:

    @allure.title("Успешный логин (используем данные созданного курьера)")
    def test_login_successful(self, courier_fixture):
        """
        1. У нас уже есть реальный курьер (courier_fixture).
        2. Логинимся с правильными логином/паролем.
        3. Ожидаем 200 и id в ответе.
        """
        # Берём валидный логин/пароль
        courier_data = courier_fixture["data"]
        payload = _create_login_payload(courier_data.login, courier_data.password)
        resp = requests.post(f"{COURIER_URL}/login", json=payload)
        assert_status_code(resp, 200, "Ожидали 200 при успешном логине")

        body = resp.json()
        assert "id" in body, f"Нет поля id в ответе: {body}"
        # Можно также проверить, что id совпадает с тем, что вернула фикстура
        assert body["id"] == courier_fixture["id"], "ID в ответе не совпадает с ожидаемым"

    @allure.title("Ошибка при отсутствии поля 'login'")
    def test_login_missing_login(self, courier_fixture):
        """
        Хоть у нас и есть реальный курьер,
        мы проверяем ситуацию, когда в запросе нет 'login'.
        Ожидаем 400 и сообщение 'Недостаточно данных для входа'.
        """
        payload = _create_login_payload(None, courier_fixture["data"].password)
        payload.pop("login")
        resp = requests.post(f"{COURIER_URL}/login", json=payload)
        assert_status_code(resp, 400, "Ожидали 400 при отсутствии логина")
        err_msg = resp.json().get("message")
        assert err_msg == "Недостаточно данных для входа", (
            f"Ожидали 'Недостаточно данных для входа', а получили: {err_msg}"
        )

    @allure.title("Ошибка при отсутствии поля 'password'")
    def test_login_missing_password(self, courier_fixture):

        payload = _create_login_payload(courier_fixture["data"].login, "")
        resp = requests.post(f"{COURIER_URL}/login", json=payload)
        assert_status_code(resp, 400, "Ожидали 400 при отсутствии пароля")
        err_msg = resp.json().get("message")
        assert err_msg == "Недостаточно данных для входа", (
            f"Ожидали 'Недостаточно данных для входа', получили: {err_msg}"
        )
    @allure.title("Ошибка при неверном логине")
    def test_login_wrong_login(self, courier_fixture):
        """
        Курьер создан (courier_fixture), но отправляем логин, которого нет.
        Ожидаем 404 (или код по спецификации).
        """
        payload = _create_login_payload("definitely_wrong_login", courier_fixture["data"].password)
        resp = requests.post(f"{COURIER_URL}/login", json=payload)
        # По доке "система вернёт ошибку" — допустим, что это 404
        assert_status_code(resp, 404, "Ожидали 404 при неверном логине")
        assert "message" in resp.json(), "Нет поля 'message' в ответе"

    @allure.title("Ошибка при неверном пароле")
    def test_login_wrong_password(self, courier_fixture):
        """
        Курьер создан (courier_fixture), но отправляем неправильный пароль.
        """
        payload = _create_login_payload(courier_fixture["data"].login, "thisIsWrong")
        resp = requests.post(f"{COURIER_URL}/login", json=payload)
        assert_status_code(resp, 404, "Ожидали 404 при неверном пароле")
        assert "message" in resp.json(), "Нет поля 'message' в ответе"

    @allure.title("Ошибка при логине несуществующего курьера (когда вообще не создаём)")
    def test_login_nonexistent_courier(self):
        """
        В этом тесте не используем fixture, потому что нам не нужен реальный курьер:
        мы хотим проверить "несуществующие логин/пароль".
        """
        payload = _create_login_payload("ghost_login_123", "ghost_pass_123")
        resp = requests.post(f"{COURIER_URL}/login", json=payload)
        assert_status_code(resp, 404, "Ожидали 404 при логине несуществующего курьера")
        msg = resp.json().get("message")
        assert msg, "Нет 'message' в ответе"