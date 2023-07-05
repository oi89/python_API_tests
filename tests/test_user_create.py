import random
import string
from datetime import datetime
import pytest
import requests

from helpers.assertions import Assertions
from helpers.base_case import BaseCase


class TestUserCreate(BaseCase):
    conditions = [
        "username",
        "firstName",
        "lastName",
        "email",
        "password"
    ]

    def setup_method(self):
        self.url_create_user = "https://playground.learnqa.ru/api/user/"

        email_base_part = "test"
        email_random_part = datetime.now().strftime("%d%m%Y%H%M%S")
        email_domain = "example.com"
        self.random_email = f"{email_base_part}{email_random_part}@{email_domain}"

        self.data = {
            "username": "test",
            "firstName": "test",
            "lastName": "test",
            "email": self.random_email,
            "password": "test",
        }

    def test_create_user_successfully(self):
        response = requests.post(url=self.url_create_user, data=self.data)

        Assertions.assert_status_code(response=response, expected_status_code=200)
        Assertions.assert_json_has_key(response=response, name="id")

    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"
        self.data["email"] = email

        response = requests.post(url=self.url_create_user, data=self.data)

        Assertions.assert_status_code(response=response, expected_status_code=400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"

    def test_create_user_with_incorrect_email(self):
        self.data["email"] = self.random_email.replace("@", "")  # email without @

        response = requests.post(url=self.url_create_user, data=self.data)

        Assertions.assert_status_code(response=response, expected_status_code=400)
        Assertions.assert_response_text(response=response, expected_text="Invalid email format")

    @pytest.mark.parametrize("condition", conditions)
    def test_create_user_without_field(self, condition):
        del self.data[condition]  # delete field from json

        response = requests.post(url=self.url_create_user, data=self.data)

        Assertions.assert_status_code(response=response, expected_status_code=400)
        Assertions.assert_response_text(
            response=response,
            expected_text=f"The following required params are missed: {condition}"
        )

    def test_create_user_with_short_username(self):
        username = "a"
        self.data["username"] = username

        response = requests.post(url=self.url_create_user, data=self.data)

        Assertions.assert_status_code(response=response, expected_status_code=400)
        Assertions.assert_response_text(response=response, expected_text="The value of 'username' field is too short")

    def test_create_user_with_long_username(self):
        str_length = 251
        username = "".join([random.choice(string.ascii_letters) for i in range(str_length)])
        self.data["username"] = username

        response = requests.post(url=self.url_create_user, data=self.data)

        Assertions.assert_status_code(response=response, expected_status_code=400)
        Assertions.assert_response_text(response=response, expected_text="The value of 'username' field is too long")
