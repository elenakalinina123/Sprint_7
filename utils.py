import random
import string

import allure
import requests

from .data import api_link


@allure.step('генерируем случайную строку')
def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


@allure.step('генерируем случайные данные курьера')
def generate_courier_data():
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    data = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    return data


@allure.step('регистрируем нового курьера')
def register_new_courier(data):
    return requests.post(f'{api_link}/courier', data=data)


@allure.step('авторизовываем курьера')
def login_courier(data):
    data.pop('firstName', None)

    return requests.post(f'{api_link}/courier/login', data=data)


@allure.step('создаем новый заказ')
def create_new_order(order_json):
    return requests.post(f'{api_link}/orders', json=order_json)


@allure.step('получаем список заказов')
def get_order_list():
    return requests.get(f'{api_link}/orders')
