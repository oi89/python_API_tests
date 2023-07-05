import requests

from helpers.base_case import BaseCase
from helpers.assertions import Assertions


class TestUserGet(BaseCase):

    def auth_by_existed_user(self, email, password):
        data = {
            "email": email,
            "password": password
        }
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        self.auth_cookie_value = self.get_cookie(response=response1, cookie_name="auth_sid")
        self.token_value = self.get_header(response=response1, header_name="x-csrf-token")
        self.user_id_from_auth = self.get_json_value(response=response1, field_name="user_id")

    def test_get_details_by_not_authorized_user(self):
        response = requests.get("https://playground.learnqa.ru/api/user/2")

        Assertions.assert_status_code(response=response, expected_status_code=200)
        Assertions.assert_json_has_key(response=response, name="username")

        not_expected_fields = ["id", "email", "firstName", "lastName"]
        Assertions.assert_json_has_no_keys(response=response, names=not_expected_fields)

    def test_get_details_by_current_authorized_user(self):
        self.auth_by_existed_user(email="vinkotov@example.com", password="1234")

        response2 = requests.get(
            f"https://playground.learnqa.ru/api/user/{self.user_id_from_auth}",
            cookies={"auth_sid": self.auth_cookie_value},
            headers={"x-csrf-token": self.token_value}
        )

        Assertions.assert_status_code(response=response2, expected_status_code=200)

        expected_fields = ["id", "username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response=response2, names=expected_fields)

    def test_get_details_by_another_authorized_user(self):
        self.auth_by_existed_user(email="vinkotov@example.com", password="1234")

        response2 = requests.get(
            "https://playground.learnqa.ru/api/user/1",  # another user id
            cookies={"auth_sid": self.auth_cookie_value},
            headers={"x-csrf-token": self.token_value}
        )

        Assertions.assert_status_code(response=response2, expected_status_code=200)
        Assertions.assert_json_has_key(response=response2, name="username")

        not_expected_fields = ["id", "email", "firstName", "lastName"]
        Assertions.assert_json_has_no_keys(response=response2, names=not_expected_fields)
