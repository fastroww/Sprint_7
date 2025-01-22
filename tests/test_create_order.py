import pytest
import allure
from conftest import assert_status_code
import requests
from constants import ORDER_URL
from testdata.order_data import generate_fake_order_data
from conftest import create_orders_fixture, cancel_orders_fixture


@allure.suite("Orders API")
@allure.sub_suite("Create order")
class TestCreateOrder:

    @allure.title("Проверяем параметризацию: разные варианты цвета")
    @pytest.mark.parametrize("colors", [
        None,
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"]
    ])
    def test_create_order_param(self, create_orders_fixture, cancel_orders_fixture, colors):
        """
        При помощи параметризации проверяем создание заказа
        - без цвета,
        - с BLACK,
        - с GREY,
        - с обоими цветами.
        """
        create_order = create_orders_fixture
        tracks = create_order(count=1, color=colors)
        assert len(tracks) == 1
        cancel_orders_fixture(tracks)

    @allure.title("Проверяем успешное создание заказа")
    def test_create_order_success(self, create_orders_fixture, cancel_orders_fixture):
        """
        Проверяем успешное создание заказа
        """
        create_order = create_orders_fixture
        tracks = create_order(count=1)
        assert len(tracks) == 1
        cancel_orders_fixture(tracks)

    @allure.title("Проверяем создание нескольких заказов")
    def test_create_multiple_orders(self, create_orders_fixture, cancel_orders_fixture):
        """
        Проверяем создание нескольких заказов
        """
        create_order = create_orders_fixture
        tracks = create_order(count=3)
        assert len(tracks) == 3
        cancel_orders_fixture(tracks)