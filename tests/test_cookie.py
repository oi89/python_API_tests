import requests

from helpers.base_case import BaseCase


class TestCookie(BaseCase):

    def test_cookie_value(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        actual_cookie_value = self.get_cookie(response=response, cookie_name="HomeWork")
        expected_cookie_value = "hw_value"

        assert actual_cookie_value == expected_cookie_value, "Cookie 'HomeWork' has incorrect value"
