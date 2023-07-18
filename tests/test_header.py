import allure
import requests

from helpers.base_case import BaseCase


@allure.epic("Headers")
class TestHeader(BaseCase):

    @allure.description("Test checks header's value from /api/homework_header")
    def test_header_value(self):
        with allure.step("GET /api/homework_header"):
            response = requests.get("https://playground.learnqa.ru/api/homework_header")
        with allure.step("Get value of 'x-secret-homework-header'"):
            actual_header_value = self.get_header(response=response, header_name="x-secret-homework-header")
            expected_header_value = "Some secret value"

        with allure.step("Check that the header has correct value"):
            assert actual_header_value == expected_header_value, "Header 'x-secret-homework-header' has incorrect value"
