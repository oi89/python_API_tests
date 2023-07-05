import requests

from helpers.assertions import Assertions
from helpers.base_case import BaseCase


class TestUserEdit(BaseCase):

    def create_new_user(self):
        self.create_data = self.get_create_user_data()
        response_create = requests.post(url="https://playground.learnqa.ru/api/user/", data=self.create_data)

        return response_create

    def login(self, email, password):
        login_data = {
            "email": email,
            "password": password
        }
        response_login = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        self.auth_cookie_value = self.get_cookie(response=response_login, cookie_name="auth_sid")
        self.token_value = self.get_header(response=response_login, header_name="x-csrf-token")

        return response_login

    def edit_user(self, user_id, data):
        response_edit = requests.put(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            cookies={"auth_sid": self.auth_cookie_value},
            headers={"x-csrf-token": self.token_value},
            data=data
        )

        return response_edit

    def get_user_info(self, user_id):
        response_get_info = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            cookies={"auth_sid": self.auth_cookie_value},
            headers={"x-csrf-token": self.token_value}
        )

        return response_get_info

    def test_user_edit_by_created_user(self):
        # Create user
        response_create = self.create_new_user()
        email = self.create_data["email"]
        password = self.create_data["password"]
        user_id = self.get_json_value(response=response_create, field_name="id")

        # Login
        response_login = self.login(email=email, password=password)

        # Edit user
        new_firstname = "new_test"
        edit_data = {"firstName": new_firstname}
        response_edit = self.edit_user(user_id=user_id, data=edit_data)

        Assertions.assert_status_code(response=response_edit, expected_status_code=200)

        # Get user info
        response_get_info = self.get_user_info(user_id=user_id)

        Assertions.assert_status_code(response=response_get_info, expected_status_code=200)
        Assertions.get_json_value_by_name(
            response=response_get_info,
            name="firstName",
            expected_value=new_firstname,
            error_message="Incorrect value in field 'firstName' after edit user data"
        )

    def test_user_edit_by_unauthorized_user(self):
        # Create user
        response_create = self.create_new_user()
        user_id = self.get_json_value(response=response_create, field_name="id")

        # Edit user without authorization
        new_firstname = "new_test"
        response_edit = requests.put(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            data={"firstName": new_firstname}
        )

        Assertions.assert_status_code(response=response_edit, expected_status_code=400)
        Assertions.assert_response_text(response=response_edit, expected_text="Auth token not supplied")

    def test_user_edit_by_another_authorized_user(self):
        # Create user
        response_create = self.create_new_user()
        user_id = self.get_json_value(response=response_create, field_name="id")

        # Login by another user
        response_login = self.login(email="vinkotov@example.com", password="1234")

        # Edit user
        new_firstname = "new_test"
        edit_data = {"firstName": new_firstname}
        response_edit = self.edit_user(user_id=user_id, data=edit_data)

        Assertions.assert_status_code(response=response_edit, expected_status_code=400)
        Assertions.assert_response_text(
            response=response_edit,
            expected_text="Please, do not edit test users with ID 1, 2, 3, 4 or 5."
        )

    def test_user_edit_with_incorrect_email(self):
        # Create user
        response_create = self.create_new_user()
        email = self.create_data["email"]
        password = self.create_data["password"]
        user_id = self.get_json_value(response=response_create, field_name="id")

        # Login
        response_login = self.login(email=email, password=password)

        # Edit user with incorrect email
        new_email = email.replace("@", "")
        edit_data = {"email": new_email}
        response_edit = self.edit_user(user_id=user_id, data=edit_data)

        Assertions.assert_status_code(response=response_edit, expected_status_code=400)
        Assertions.assert_response_text(
            response=response_edit,
            expected_text="Invalid email format"
        )

    def test_user_edit_with_short_firstname(self):
        # Create user
        response_create = self.create_new_user()
        email = self.create_data["email"]
        password = self.create_data["password"]
        user_id = self.get_json_value(response=response_create, field_name="id")

        # Login
        response_login = self.login(email=email, password=password)

        # Edit user with too short firstName
        new_firstname = "t"
        edit_data = {"firstName": new_firstname}
        response_edit = self.edit_user(user_id=user_id, data=edit_data)

        Assertions.assert_status_code(response=response_edit, expected_status_code=400)
        Assertions.get_json_value_by_name(
            response=response_edit,
            name="error",
            expected_value="Too short value for field firstName",
            error_message="Incorrect value in field 'error'"
        )
