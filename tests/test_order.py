from http import HTTPStatus

import allure
import pytest

from ..data import order_json
from ..utils import create_new_order, get_order_list


class TestOrder:
    @allure.title('Тест на успешное создание заказа')
    @pytest.mark.parametrize('colors', [
        {'color': []},
        {'color': ['GRAY']},
        {'color': ['BLACK']},
        {'color': ['GRAY', 'BLACK']},
    ])
    def test_create_order(self, colors):
        order_json.update(colors)

        response = create_new_order(order_json)

        assert response.status_code == HTTPStatus.CREATED
        assert 'track' in response.text


class TestOrderList:
    @allure.title('Тест получения списка заказов')
    def test_order_list(self):
        response = get_order_list()

        assert response.status_code == HTTPStatus.OK
        assert 'orders' and 'id' in response.text
