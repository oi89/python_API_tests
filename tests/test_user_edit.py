import allure

from helpers.assertions import Assertions
from helpers.base_case import BaseCase
from helpers.my_requests import MyRequests


@allure.epic("Edit a user")
class TestUserEdit(BaseCase):

    @allure.step("Create a new user")
    def create_new_user(self):
        self.create_data = self.get_create_user_data()
        response_create = MyRequests.post(uri="/user/", data=self.create_data)

        return response_create

    def edit_user(self, user_id, data):
        response_edit = MyRequests.put(
            uri=f"/user/{user_id}",
            cookies={"auth_sid": self.auth_cookie_value},
            headers={"x-csrf-token": self.token_value},
            data=data
        )

        return response_edit

    @allure.description("Test checks that firstName can be edited from authorized user")
    def test_edit_user_by_created_user(self):
        # Create user
        self.create_new_user()
        email = self.create_data["email"]
        password = self.create_data["password"]

        # Login
        self.login(email=email, password=password)

        with allure.step("Edit user"):
            new_firstname = "new_test"
            edit_data = {"firstName": new_firstname}
            response_edit = self.edit_user(user_id=self.user_id, data=edit_data)

        with allure.step("Check that status code = 200"):
            Assertions.assert_status_code(response=response_edit, expected_status_code=200)

        # Get user info
        response_get_info = self.get_user_info(user_id=self.user_id)

        with allure.step("Check that status code = 200 and field 'firstName' has correct value"):
            Assertions.assert_status_code(response=response_get_info, expected_status_code=200)
            Assertions.get_json_value_by_name(
                response=response_get_info,
                name="firstName",
                expected_value=new_firstname,
                error_message="Incorrect value in field 'firstName' after edit user data"
            )

    @allure.description("Test checks that firstName cannot be edited from unauthorized user")
    def test_edit_user_by_unauthorized_user(self):
        # Create user
        response_create = self.create_new_user()
        user_id = self.get_json_value(response=response_create, field_name="id")

        with allure.step("Edit user without authorization"):
            new_firstname = "new_test"
            response_edit = MyRequests.put(
                uri=f"/user/{user_id}",
                data={"firstName": new_firstname}
            )

        with allure.step("Check that status code = 400 and response has the correct text"):
            Assertions.assert_status_code(response=response_edit, expected_status_code=400)
            Assertions.assert_response_text(response=response_edit, expected_text="Auth token not supplied")

    @allure.description("Test checks that firstName cannot be edited from another authorized user")
    def test_edit_user_by_another_authorized_user(self):
        # Create user
        response_create = self.create_new_user()
        user_id = self.get_json_value(response=response_create, field_name="id")

        # Login by another user
        self.login(email="vinkotov@example.com", password="1234")

        with allure.step("Edit created user by another user"):
            new_firstname = "new_test"
            edit_data = {"firstName": new_firstname}
            response_edit = self.edit_user(user_id=user_id, data=edit_data)

        with allure.step("Check that status code = 400 and response has the correct text"):
            Assertions.assert_status_code(response=response_edit, expected_status_code=400)
            Assertions.assert_response_text(
                response=response_edit,
                expected_text="Please, do not edit test users with ID 1, 2, 3, 4 or 5."
            )

    @allure.description("Test checks that email cannot be replaced with incorrect email")
    def test_edit_user_with_incorrect_email(self):
        # Create user
        self.create_new_user()
        email = self.create_data["email"]
        password = self.create_data["password"]

        # Login
        self.login(email=email, password=password)

        with allure.step("Edit user with incorrect email"):
            new_email = email.replace("@", "")
            edit_data = {"email": new_email}
            response_edit = self.edit_user(user_id=self.user_id, data=edit_data)

        with allure.step("Check that status code = 400 and response has the correct text"):
            Assertions.assert_status_code(response=response_edit, expected_status_code=400)
            Assertions.assert_response_text(
                response=response_edit,
                expected_text="Invalid email format"
            )

    @allure.description("Test checks that firstName cannot be replaced with a string contains 1 symbol")
    def test_edit_user_with_short_firstname(self):
        # Create user
        self.create_new_user()
        email = self.create_data["email"]
        password = self.create_data["password"]

        # Login
        self.login(email=email, password=password)

        with allure.step("Edit user with too short firstName"):
            new_firstname = "t"
            edit_data = {"firstName": new_firstname}
            response_edit = self.edit_user(user_id=self.user_id, data=edit_data)

        with allure.step("Check that status code = 400 and response has the correct text"):
            Assertions.assert_status_code(response=response_edit, expected_status_code=400)
            Assertions.get_json_value_by_name(
                response=response_edit,
                name="error",
                expected_value="Too short value for field firstName",
                error_message="Incorrect value in field 'error'"
            )
