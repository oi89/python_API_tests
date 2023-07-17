import random
import string
import pytest

from helpers.assertions import Assertions
from helpers.base_case import BaseCase
from helpers.my_requests import MyRequests


class TestUserCreate(BaseCase):
    uri_create_user = "/user/"

    conditions = [
        "username",
        "firstName",
        "lastName",
        "email",
        "password"
    ]

    def create_user(self, data):
        response_create = MyRequests.post(uri=self.uri_create_user, data=data)

        return response_create

    def test_create_user_successfully(self):
        response_create = self.create_user(data=self.get_create_user_data())

        Assertions.assert_status_code(response=response_create, expected_status_code=200)
        Assertions.assert_json_has_key(response=response_create, name="id")

    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"
        data = self.get_create_user_data(email=email)

        response_create = self.create_user(data=data)

        Assertions.assert_status_code(response=response_create, expected_status_code=400)
        assert response_create.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response_create.content}"

    def test_create_user_with_incorrect_email(self):
        data = self.get_create_user_data()
        data["email"] = data["email"].replace("@", "")  # email without @

        response_create = self.create_user(data=data)

        Assertions.assert_status_code(response=response_create, expected_status_code=400)
        Assertions.assert_response_text(response=response_create, expected_text="Invalid email format")

    @pytest.mark.parametrize("condition", conditions)
    def test_create_user_without_field(self, condition):
        data = self.get_create_user_data()
        del data[condition]  # delete field from json

        response_create = self.create_user(data=data)

        Assertions.assert_status_code(response=response_create, expected_status_code=400)
        Assertions.assert_response_text(
            response=response_create,
            expected_text=f"The following required params are missed: {condition}"
        )

    def test_create_user_with_short_username(self):
        username = "a"
        data = self.get_create_user_data()
        data["username"] = username

        response_create = self.create_user(data=data)

        Assertions.assert_status_code(response=response_create, expected_status_code=400)
        Assertions.assert_response_text(
            response=response_create,
            expected_text="The value of 'username' field is too short"
        )

    def test_create_user_with_long_username(self):
        str_length = 251
        username = "".join([random.choice(string.ascii_letters) for i in range(str_length)])
        data = self.get_create_user_data()
        data["username"] = username

        response_create = self.create_user(data=data)

        Assertions.assert_status_code(response=response_create, expected_status_code=400)
        Assertions.assert_response_text(
            response=response_create,
            expected_text="The value of 'username' field is too long"
        )
