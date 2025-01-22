import requests
import allure

from constants import ORDER_URL

@allure.suite("Orders API")
@allure.sub_suite("Get orders list")
class TestGetOrdersList:


    @allure.title("Проверяем, что GET /orders без параметров возвращает код 200 и поле 'orders' (список)")
    def test_get_orders_no_params_returns_list(self):
        """
        1. Делаем GET /api/v1/orders
        2. Проверяем код = 200.
        3. Проверяем, что в ответе есть ключ 'orders' и он является списком.
        """
        response = requests.get(ORDER_URL)
        assert response.status_code == 200, (
            f"Ожидали 200, а получили {response.status_code}: {response.text}"
        )

        body = response.json()
        assert "orders" in body, f"Нет ключа 'orders' в ответе: {body}"
        assert isinstance(body["orders"], list), "Поле 'orders' должно быть списком"