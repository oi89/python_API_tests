from helpers.base_case import BaseCase
from helpers.assertions import Assertions
from helpers.my_requests import MyRequests


class TestUserGet(BaseCase):

    def test_get_details_by_not_authorized_user(self):
        response_get = MyRequests.get(uri="/user/2")

        Assertions.assert_status_code(response=response_get, expected_status_code=200)
        Assertions.assert_json_has_key(response=response_get, name="username")

        not_expected_fields = ["id", "email", "firstName", "lastName"]
        Assertions.assert_json_has_no_keys(response=response_get, names=not_expected_fields)

    def test_get_details_by_current_authorized_user(self):
        self.login(email="vinkotov@example.com", password="1234")

        response_get = self.get_user_info(user_id=self.user_id)

        Assertions.assert_status_code(response=response_get, expected_status_code=200)

        expected_fields = ["id", "username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response=response_get, names=expected_fields)

    def test_get_details_by_another_authorized_user(self):
        self.login(email="vinkotov@example.com", password="1234")

        response_get = self.get_user_info(1)  # another user id

        Assertions.assert_status_code(response=response_get, expected_status_code=200)
        Assertions.assert_json_has_key(response=response_get, name="username")

        not_expected_fields = ["id", "email", "firstName", "lastName"]
        Assertions.assert_json_has_no_keys(response=response_get, names=not_expected_fields)
