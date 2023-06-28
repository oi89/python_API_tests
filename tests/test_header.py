import requests

from helpers.base_case import BaseCase


class TestHeader(BaseCase):

    def test_header_value(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        actual_header_value = self.get_header(response=response, header_name="x-secret-homework-header")
        expected_header_value = "Some secret value"

        assert actual_header_value == expected_header_value, "Header 'x-secret-homework-header' has incorrect value"
