import pytest
import requests

from lib.base_case import BaseCase


class TestUserAuth(BaseCase):
    conditions = [
        ("no_cookie"),
        ("no_header"),
        ("no_cookie_and_header")
    ]

    def setup_method(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        self.auth_cookie_value = self.get_cookie(response=response1, cookie_name="auth_sid")
        self.token_value = self.get_header(response=response1, header_name="x-csrf-token")
        self.user_id_from_auth = self.get_json_value(response=response1, field_name="user_id")

    def test_user_auth(self):
        response2 = requests.get(
            url="https://playground.learnqa.ru/api/user/auth",
            cookies={"auth_sid": self.auth_cookie_value},
            headers={"x-csrf-token": self.token_value}
        )

        assert "user_id" in response2.json(), "There is no field 'user_id' in the check response body"

        user_id_from_check = response2.json()["user_id"]

        assert self.user_id_from_auth == user_id_from_check, "User id from auth API isn't equal to user id from check API"

    @pytest.mark.parametrize("condition", conditions)
    def test_negative_auth(self, condition):
        if condition == "no_cookie":
            response2 = requests.get(
                url="https://playground.learnqa.ru/api/user/auth",
                headers={"x-csrf-token": self.token_value}
            )
        elif condition == "no_header":
            response2 = requests.get(
                url="https://playground.learnqa.ru/api/user/auth",
                cookies={"auth_sid": self.auth_cookie_value}
            )
        else:
            response2 = requests.get(
                url="https://playground.learnqa.ru/api/user/auth"
            )

        assert "user_id" in response2.json(), "There is no field 'user_id' in the check response body"

        user_id_from_check = response2.json()["user_id"]

        assert user_id_from_check == 0, f"User is authorized with condition {condition}"
