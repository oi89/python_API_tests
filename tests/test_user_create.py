import random
import string

import allure
import pytest

from helpers.assertions import Assertions
from helpers.base_case import BaseCase
from helpers.my_requests import MyRequests


@allure.epic("Create a user")
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

    @allure.description("Test checks that user can be created")
    def test_create_user_successfully(self):
        with allure.step("Create a user"):
            response_create = self.create_user(data=self.get_create_user_data())

        with allure.step("Check that status code = 200 and field 'id' exists in the response"):
            Assertions.assert_status_code(response=response_create, expected_status_code=200)
            Assertions.assert_json_has_key(response=response_create, name="id")

    @allure.description("Test checks that user cannot be created with existing email")
    def test_create_user_with_existing_email(self):
        with allure.step("Generate user data"):
            email = "vinkotov@example.com"
            data = self.get_create_user_data(email=email)

        with allure.step("Create a user with existing email"):
            response_create = self.create_user(data=data)

        with allure.step("Check that status code = 400 and response has the correct text"):
            Assertions.assert_status_code(response=response_create, expected_status_code=400)
            assert response_create.content.decode("utf-8") == f"Users with email '{email}' already exists", \
                f"Unexpected response content {response_create.content}"

    @allure.description("Test checks that user cannot be created with incorrect email")
    def test_create_user_with_incorrect_email(self):
        with allure.step("Generate user data"):
            data = self.get_create_user_data()
            data["email"] = data["email"].replace("@", "")  # email without @

        with allure.step("Create a user with incorrect email"):
            response_create = self.create_user(data=data)

        with allure.step("Check that status code = 400 and response has the correct text"):
            Assertions.assert_status_code(response=response_create, expected_status_code=400)
            Assertions.assert_response_text(response=response_create, expected_text="Invalid email format")

    @allure.description("Test checks that user cannot be created with incorrect email")
    @pytest.mark.parametrize("condition", conditions)
    def test_create_user_without_field(self, condition):
        with allure.step("Generate user data"):
            data = self.get_create_user_data()
            del data[condition]  # delete field from json

        with allure.step(f"Create a user without field '{condition}'"):
            response_create = self.create_user(data=data)

        with allure.step("Check that status code = 400 and response has the correct text"):
            Assertions.assert_status_code(response=response_create, expected_status_code=400)
            Assertions.assert_response_text(
                response=response_create,
                expected_text=f"The following required params are missed: {condition}"
            )

    @allure.description("Test checks that user cannot be created when username contains 1 symbol")
    def test_create_user_with_short_username(self):
        with allure.step("Generate user data"):
            username = "a"
            data = self.get_create_user_data()
            data["username"] = username

        with allure.step("Create a user with a short username"):
            response_create = self.create_user(data=data)

        with allure.step("Check that status code = 400 and response has the correct text"):
            Assertions.assert_status_code(response=response_create, expected_status_code=400)
            Assertions.assert_response_text(
                response=response_create,
                expected_text="The value of 'username' field is too short"
            )

    @allure.description("Test checks that user cannot be created when username contains 251 symbol")
    def test_create_user_with_long_username(self):
        with allure.step("Generate user data"):
            str_length = 251
            username = "".join([random.choice(string.ascii_letters) for i in range(str_length)])
            data = self.get_create_user_data()
            data["username"] = username

        with allure.step("Create a user with a long username"):
            response_create = self.create_user(data=data)

        with allure.step("Check that status code = 400 and response has the correct text"):
            Assertions.assert_status_code(response=response_create, expected_status_code=400)
            Assertions.assert_response_text(
                response=response_create,
                expected_text="The value of 'username' field is too long"
            )
