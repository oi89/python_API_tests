import allure

from helpers.assertions import Assertions
from helpers.base_case import BaseCase
from helpers.my_requests import MyRequests


@allure.epic("Delete a user")
class TestUserDelete(BaseCase):

    @allure.step("Create a new user")
    def create_new_user(self):
        self.create_data = self.get_create_user_data()
        response_create = MyRequests.post(uri="/user/", data=self.create_data)

        return response_create

    def delete_user(self, user_id):
        response_delete = MyRequests.delete(
            uri=f"/user/{user_id}",
            cookies={"auth_sid": self.auth_cookie_value},
            headers={"x-csrf-token": self.token_value}
        )

        return response_delete

    @allure.description("Test checks that predefined user cannot be deleted")
    def test_delete_forbidden_user(self):
        email = "vinkotov@example.com"
        password = "1234"

        # Login
        self.login(email=email, password=password)

        with allure.step("Delete the forbidden user"):
            response_delete = self.delete_user(self.user_id)

        with allure.step("Check that status code = 400 and response has the correct text"):
            Assertions.assert_status_code(response=response_delete, expected_status_code=400)
            Assertions.assert_response_text(
                response=response_delete,
                expected_text="Please, do not delete test users with ID 1, 2, 3, 4 or 5."
            )

    @allure.description("Test checks that created user can be deleted")
    def test_delete_created_user(self):
        # Create user
        self.create_new_user()
        email = self.create_data["email"]
        password = self.create_data["password"]

        # Login
        self.login(email=email, password=password)

        with allure.step("Delete user"):
            response_delete = self.delete_user(user_id=self.user_id)

        with allure.step("Check that status code = 200"):
            Assertions.assert_status_code(response=response_delete, expected_status_code=200)

        # Get user info
        response_get_info = self.get_user_info(user_id=self.user_id)

        with allure.step("Check that status code = 404 and response has the correct text"):
            Assertions.assert_status_code(response=response_get_info, expected_status_code=404)
            Assertions.assert_response_text(
                response=response_get_info,
                expected_text="User not found"
            )

    @allure.description("Test checks that another user cannot be deleted")
    def test_delete_user_by_another_authorized_user(self):
        # Create user
        response_create = self.create_new_user()
        user_id = self.get_json_value(response=response_create, field_name="id")

        # Login by another user
        self.login(email="vinkotov@example.com", password="1234")

        with allure.step("Delete another user"):
            response_delete = self.delete_user(user_id=user_id)

        with allure.step("Check that status code = 400 and response has the correct text"):
            Assertions.assert_status_code(response=response_delete, expected_status_code=400)
            Assertions.assert_response_text(
                response=response_delete,
                expected_text="Please, do not delete test users with ID 1, 2, 3, 4 or 5."
            )
