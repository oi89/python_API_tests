import allure
from requests import Response
from json.decoder import JSONDecodeError
from datetime import datetime

from helpers.my_requests import MyRequests


class BaseCase:

    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"There is no cookie '{cookie_name}' in the response"

        return response.cookies.get(cookie_name)

    def get_header(self, response: Response, header_name):
        assert header_name in response.headers, f"There is no header '{header_name}' in the response"

        return response.headers.get(header_name)

    def get_json_value(self, response: Response, field_name):
        try:
            json_dict = response.json()
        except JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert field_name in json_dict, f"Response JSON doesn't have the key '{field_name}'"

        return json_dict[field_name]

    def get_create_user_data(self, email=None):
        if email is None:
            email_base_part = "test"
            email_random_part = datetime.now().strftime("%d%m%Y%H%M%S")
            email_domain = "example.com"
            email = f"{email_base_part}{email_random_part}@{email_domain}"

        return {
            "username": "test",
            "firstName": "test",
            "lastName": "test",
            "email": email,
            "password": "test",
        }

    @allure.step("Login a user with email = '{email}'")
    def login(self, email, password):
        login_data = {
            "email": email,
            "password": password
        }
        response_login = MyRequests.post(uri="/user/login", data=login_data)

        self.auth_cookie_value = self.get_cookie(response=response_login, cookie_name="auth_sid")
        self.token_value = self.get_header(response=response_login, header_name="x-csrf-token")
        self.user_id = self.get_json_value(response=response_login, field_name="user_id")

        return response_login

    @allure.step("Get user info by id '{user_id}'")
    def get_user_info(self, user_id):
        response_get_info = MyRequests.get(
            uri=f"/user/{user_id}",
            cookies={"auth_sid": self.auth_cookie_value},
            headers={"x-csrf-token": self.token_value}
        )

        return response_get_info
