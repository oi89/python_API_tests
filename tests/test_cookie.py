import allure
import requests

from helpers.base_case import BaseCase


@allure.epic("Cookies")
class TestCookie(BaseCase):

    @allure.description("Test checks cookie's value from /api/homework_cookie")
    def test_cookie_value(self):
        with allure.step("GET /api/homework_cookie"):
            response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        with allure.step("Get value of cookie 'HomeWork'"):
            actual_cookie_value = self.get_cookie(response=response, cookie_name="HomeWork")
            expected_cookie_value = "hw_value"

        with allure.step("Check that the cookie has correct value"):
            assert actual_cookie_value == expected_cookie_value, "Cookie 'HomeWork' has incorrect value"
