import random
import string
import pytest
import requests

from helpers.assertions import Assertions
from helpers.base_case import BaseCase


class TestUserCreate(BaseCase):
    url_create_user = "https://playground.learnqa.ru/api/user/"

    conditions = [
        "username",
        "firstName",
        "lastName",
        "email",
        "password"
    ]

    def test_create_user_successfully(self):
        response = requests.post(url=self.url_create_user, data=self.get_create_user_data())

        Assertions.assert_status_code(response=response, expected_status_code=200)
        Assertions.assert_json_has_key(response=response, name="id")

    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"
        data = self.get_create_user_data(email=email)

        response = requests.post(url=self.url_create_user, data=data)

        Assertions.assert_status_code(response=response, expected_status_code=400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"

    def test_create_user_with_incorrect_email(self):
        data = self.get_create_user_data()
        data["email"] = data["email"].replace("@", "")  # email without @

        response = requests.post(url=self.url_create_user, data=data)

        Assertions.assert_status_code(response=response, expected_status_code=400)
        Assertions.assert_response_text(response=response, expected_text="Invalid email format")

    @pytest.mark.parametrize("condition", conditions)
    def test_create_user_without_field(self, condition):
        data = self.get_create_user_data()
        del data[condition]  # delete field from json

        response = requests.post(url=self.url_create_user, data=data)

        Assertions.assert_status_code(response=response, expected_status_code=400)
        Assertions.assert_response_text(
            response=response,
            expected_text=f"The following required params are missed: {condition}"
        )

    def test_create_user_with_short_username(self):
        username = "a"
        data = self.get_create_user_data()
        data["username"] = username

        response = requests.post(url=self.url_create_user, data=data)

        Assertions.assert_status_code(response=response, expected_status_code=400)
        Assertions.assert_response_text(response=response, expected_text="The value of 'username' field is too short")

    def test_create_user_with_long_username(self):
        str_length = 251
        username = "".join([random.choice(string.ascii_letters) for i in range(str_length)])
        data = self.get_create_user_data()
        data["username"] = username

        response = requests.post(url=self.url_create_user, data=data)

        Assertions.assert_status_code(response=response, expected_status_code=400)
        Assertions.assert_response_text(response=response, expected_text="The value of 'username' field is too long")
