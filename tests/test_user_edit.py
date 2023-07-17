from helpers.assertions import Assertions
from helpers.base_case import BaseCase
from helpers.my_requests import MyRequests


class TestUserEdit(BaseCase):

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

    def test_edit_user_by_created_user(self):
        # Create user
        self.create_new_user()
        email = self.create_data["email"]
        password = self.create_data["password"]

        # Login
        self.login(email=email, password=password)

        # Edit user
        new_firstname = "new_test"
        edit_data = {"firstName": new_firstname}
        response_edit = self.edit_user(user_id=self.user_id, data=edit_data)

        Assertions.assert_status_code(response=response_edit, expected_status_code=200)

        # Get user info
        response_get_info = self.get_user_info(user_id=self.user_id)

        Assertions.assert_status_code(response=response_get_info, expected_status_code=200)
        Assertions.get_json_value_by_name(
            response=response_get_info,
            name="firstName",
            expected_value=new_firstname,
            error_message="Incorrect value in field 'firstName' after edit user data"
        )

    def test_edit_user_by_unauthorized_user(self):
        # Create user
        response_create = self.create_new_user()
        user_id = self.get_json_value(response=response_create, field_name="id")

        # Edit user without authorization
        new_firstname = "new_test"
        response_edit = MyRequests.put(
            uri=f"/user/{user_id}",
            data={"firstName": new_firstname}
        )

        Assertions.assert_status_code(response=response_edit, expected_status_code=400)
        Assertions.assert_response_text(response=response_edit, expected_text="Auth token not supplied")

    def test_edit_user_by_another_authorized_user(self):
        # Create user
        response_create = self.create_new_user()
        user_id = self.get_json_value(response=response_create, field_name="id")

        # Login by another user
        self.login(email="vinkotov@example.com", password="1234")

        # Edit user
        new_firstname = "new_test"
        edit_data = {"firstName": new_firstname}
        response_edit = self.edit_user(user_id=user_id, data=edit_data)

        Assertions.assert_status_code(response=response_edit, expected_status_code=400)
        Assertions.assert_response_text(
            response=response_edit,
            expected_text="Please, do not edit test users with ID 1, 2, 3, 4 or 5."
        )

    def test_edit_user_with_incorrect_email(self):
        # Create user
        self.create_new_user()
        email = self.create_data["email"]
        password = self.create_data["password"]

        # Login
        self.login(email=email, password=password)

        # Edit user with incorrect email
        new_email = email.replace("@", "")
        edit_data = {"email": new_email}
        response_edit = self.edit_user(user_id=self.user_id, data=edit_data)

        Assertions.assert_status_code(response=response_edit, expected_status_code=400)
        Assertions.assert_response_text(
            response=response_edit,
            expected_text="Invalid email format"
        )

    def test_edit_user_with_short_firstname(self):
        # Create user
        self.create_new_user()
        email = self.create_data["email"]
        password = self.create_data["password"]

        # Login
        self.login(email=email, password=password)

        # Edit user with too short firstName
        new_firstname = "t"
        edit_data = {"firstName": new_firstname}
        response_edit = self.edit_user(user_id=self.user_id, data=edit_data)

        Assertions.assert_status_code(response=response_edit, expected_status_code=400)
        Assertions.get_json_value_by_name(
            response=response_edit,
            name="error",
            expected_value="Too short value for field firstName",
            error_message="Incorrect value in field 'error'"
        )
