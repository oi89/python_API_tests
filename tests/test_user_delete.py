import requests

from helpers.assertions import Assertions
from helpers.base_case import BaseCase


class TestUserDelete(BaseCase):

    def create_new_user(self):
        self.create_data = self.get_create_user_data()
        response_create = requests.post(url="https://playground.learnqa.ru/api/user/", data=self.create_data)

        return response_create

    def delete_user(self, user_id):
        response_delete = requests.delete(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            cookies={"auth_sid": self.auth_cookie_value},
            headers={"x-csrf-token": self.token_value}
        )

        return response_delete

    def test_delete_forbidden_user(self):
        email = "vinkotov@example.com"
        password = "1234"

        # Login
        self.login(email=email, password=password)

        # Delete the forbidden user
        response_delete = self.delete_user(self.user_id)

        Assertions.assert_status_code(response=response_delete, expected_status_code=400)
        Assertions.assert_response_text(
            response=response_delete,
            expected_text="Please, do not delete test users with ID 1, 2, 3, 4 or 5."
        )

    def test_delete_created_user(self):
        # Create user
        self.create_new_user()
        email = self.create_data["email"]
        password = self.create_data["password"]

        # Login
        self.login(email=email, password=password)

        # Delete user
        response_delete = self.delete_user(user_id=self.user_id)

        Assertions.assert_status_code(response=response_delete, expected_status_code=200)

        # Get user info
        response_get_info = self.get_user_info(user_id=self.user_id)

        Assertions.assert_status_code(response=response_get_info, expected_status_code=404)
        Assertions.assert_response_text(
            response=response_get_info,
            expected_text="User not found"
        )

    def test_delete_user_by_another_authorized_user(self):
        # Create user
        response_create = self.create_new_user()
        user_id = self.get_json_value(response=response_create, field_name="id")

        # Login by another user
        self.login(email="vinkotov@example.com", password="1234")

        # Delete user
        response_delete = self.delete_user(user_id=user_id)

        Assertions.assert_status_code(response=response_delete, expected_status_code=400)
        Assertions.assert_response_text(
            response=response_delete,
            expected_text="Please, do not delete test users with ID 1, 2, 3, 4 or 5."
        )
