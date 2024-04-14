from http import HTTPStatus

import allure
import pytest

from ..utils import generate_courier_data, register_new_courier


class TestCreation:
    @allure.title('Тест успешной регистрации курьера')
    def test_succesfull_creation(self):
        data = generate_courier_data()
        response = register_new_courier(data)

        assert response.status_code == HTTPStatus.CREATED
        assert response.text == '{"ok":true}'

    @allure.title('Тест на регистрация двух одинаковых курьеров')
    def test_two_identical_logins(self):
        data = generate_courier_data()
        register_new_courier(data)
        response = register_new_courier(data)

        expected_error = 'Этот логин уже используется. Попробуйте другой.'

        assert response.status_code == HTTPStatus.CONFLICT
        assert expected_error in response.text

    @allure.title('Тест на проваленную регистрацию из-за отсутствия поля')
    @pytest.mark.parametrize('missing_field', ['login', 'password'])
    def test_missing_field(self, missing_field):
        data = generate_courier_data()
        del data[missing_field]
        response = register_new_courier(data)

        expected_error = 'Недостаточно данных для создания учетной записи'

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert expected_error in response.text
