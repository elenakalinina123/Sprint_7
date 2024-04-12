from http import HTTPStatus

import allure
import pytest

from ..utils import generate_courier_data, login_courier, register_new_courier


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

        assert response.status_code == HTTPStatus.CONFLICT

    @allure.title('Тест на проваленную регистрацию из-за отсутствия поля')
    @pytest.mark.parametrize('missing_field', ['login', 'password'])
    def test_missing_field(self, missing_field):
        data = generate_courier_data()
        data.pop(missing_field)
        response = register_new_courier(data)

        assert response.status_code == HTTPStatus.BAD_REQUEST


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

        assert response.status_code == HTTPStatus.BAD_REQUEST

    @allure.title('Тест логина неизвестного юзернейма')
    def test_login_unknown_user(self):
        data = generate_courier_data()
        response = login_courier(data)

        assert response.status_code == HTTPStatus.NOT_FOUND
