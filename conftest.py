import pytest
import requests
from constants import COURIER_URL, ORDER_URL, ORDER_CANCEL_URL
from testdata.courier_data import generate_courier_data
from testdata.order_data import generate_fake_order_data


def assert_status_code(response, expected_code, message=""):
    """Общая функция для проверки кода ответа и вывода ошибки"""
    assert response.status_code == expected_code, (
        f"Error: {message}. Code: {response.status_code}, Body: {response.text}"
    )


@pytest.fixture
def courier_fixture():
    """Фикстура для создания, логина и удаления курьера."""
    # 1. Генерируем данные (login, password, firstName)
    courier_data = generate_courier_data()
    payload = {
        "login": courier_data.login,
        "password": courier_data.password,
        "firstName": courier_data.firstName
    }

    # 2. Делаем POST-запрос на создание курьера
    create_response = requests.post(COURIER_URL, json=payload)
    assert_status_code(create_response, 201, "Failed to create courier")

    # 3. Логинимся, чтобы получить id (документация говорит, что id возвращается при логине)
    login_response = requests.post(f"{COURIER_URL}/login", json={
        "login": courier_data.login,
        "password": courier_data.password
    })
    assert_status_code(login_response, 200, "Failed to login courier")
    courier_id = login_response.json().get("id")
    assert courier_id is not None, f"Failed to get courier ID: {login_response.text}"

    # Передаём в тест информацию о курьере
    yield {
        "data": courier_data,  # объект с логином/паролем
        "id": courier_id  # id, полученный после логина
    }

    # ---------- Teardown: удаляем курьера ----------
    delete_response = requests.delete(f"{COURIER_URL}/{courier_id}")
    if delete_response.status_code != 200:
        print(
            f"Failed to delete courier {courier_id}. Code: {delete_response.status_code}, body: {delete_response.text}")



@pytest.fixture
def create_orders_fixture():
    """
    Фикстура, которая позволяет создавать заказы (POST /orders) перед тестом.
    """
    created_tracks = []

    def _create_order(count=1, color=None):
        """
        Вспомогательная функция для создания нескольких (count) заказов.
        :param count: сколько заказов создать
        :param color: список цветов (["BLACK"] и т.д.), если нужно
        :return: список созданных треков
        """
        for _ in range(count):
            payload = generate_fake_order_data(color=color)
            create_resp = requests.post(ORDER_URL, json=payload)
            assert_status_code(create_resp, 201, "Failed to create order")
            track = create_resp.json().get("track")
            assert track, f"Track not returned: {create_resp.text}"
            created_tracks.append(track)
        return created_tracks

    # Возвращаем функцию-создатель
    yield _create_order

    # ----- Teardown: Ничего не делаем -----

@pytest.fixture
def cancel_orders_fixture():
    """Фикстура для отмены заказов (PUT /orders/cancel) в конце."""
    created_tracks = []

    def _cancel_orders(tracks_to_cancel):
        for track in tracks_to_cancel:
            cancel_resp = requests.put(ORDER_CANCEL_URL, json={"track": track})
            # По документации успешный ответ = 200, { "ok": true }
            if cancel_resp.status_code == 200:
                print(f"Order with track {track} successfully canceled")
            else:
                print(
                    f"[WARNING] Failed to cancel order with track {track}. "
                    f"Code: {cancel_resp.status_code}, body: {cancel_resp.text}"
                )
    yield _cancel_orders
