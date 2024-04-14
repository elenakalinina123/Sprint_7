from http import HTTPStatus

import allure
import pytest

from ..utils import generate_courier_data, login_courier, register_new_courier


class TestLogin:
    @allure.title('Тест на успешный логин')
    def test_login_succesfull(self):
        data = generate_courier_data()
        response = register_new_courier(data)
        assert response.status_code == HTTPStatus.CREATED
        response = login_courier(data)

        assert response.status_code == HTTPStatus.OK
        assert 'id' in response.text

    @allure.title('Тест логина при отсутствующем поле')
    @pytest.mark.parametrize('missing_field', ['login', 'password'])
    def test_login_missing_field(self, missing_field):
        data = generate_courier_data()
        data[missing_field] = ''
        response = login_courier(data)

        expected_error = 'Недостаточно данных для входа'

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert expected_error in response.text

    @allure.title('Тест логина неизвестного юзернейма')
    def test_login_unknown_user(self):
        data = generate_courier_data()
        response = login_courier(data)

        expected_error = 'Учетная запись не найдена'

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert expected_error in response.text
