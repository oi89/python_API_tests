import allure
import pytest

from helpers.base_case import BaseCase
from helpers.assertions import Assertions
from helpers.my_requests import MyRequests


@allure.epic("Authorization")
class TestUserAuth(BaseCase):
    uri_auth_user = "/user/auth"

    conditions = [
        ("no_cookie"),
        ("no_header"),
        ("no_cookie_and_header")
    ]

    def setup_method(self):
        self.login(email="vinkotov@example.com", password="1234")

    def auth_user(self):
        response_auth = MyRequests.get(
            uri=self.uri_auth_user,
            cookies={"auth_sid": self.auth_cookie_value},
            headers={"x-csrf-token": self.token_value}
        )

        return response_auth

    @allure.description("Test checks that user_id from auth api is the same to login api")
    def test_user_auth(self):
        with allure.step("Authorize a user"):
            response_auth = self.auth_user()

        with allure.step("Check that the 'user_id' from auth method is equal to login method"):
            Assertions.get_json_value_by_name(
                response=response_auth,
                name="user_id",
                expected_value=self.user_id,
                error_message="User id from auth API isn't equal to user id from check API"
            )

    @allure.description("Test checks that user_id is 0 for a request without cookie or header")
    @pytest.mark.parametrize("condition", conditions)
    def test_negative_auth(self, condition):
        if condition == "no_cookie":
            with allure.step("Authorize a user without 'auth_sid' cookie"):
                response_auth = MyRequests.get(
                    uri=self.uri_auth_user,
                    headers={"x-csrf-token": self.token_value}
                )
        elif condition == "no_header":
            with allure.step("Authorize a user without 'x-csrf-token'"):
                response_auth = MyRequests.get(
                    uri=self.uri_auth_user,
                    cookies={"auth_sid": self.auth_cookie_value}
                )
        else:
            with allure.step("Authorize a user without both 'x-csrf-token' and 'auth_sid' cookie"):
                response_auth = MyRequests.get(
                    uri=self.uri_auth_user
                )

        with allure.step("Check that the response from auth method returns 0 for 'user_id'"):
            Assertions.get_json_value_by_name(
                response=response_auth,
                name="user_id",
                expected_value=0,
                error_message=f"User is authorized with condition {condition}"
            )
