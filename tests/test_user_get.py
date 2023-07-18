import allure

from helpers.base_case import BaseCase
from helpers.assertions import Assertions
from helpers.my_requests import MyRequests


@allure.epic("Get a user")
class TestUserGet(BaseCase):

    @allure.description("Test checks that user details contains only username for unauthorized request")
    def test_get_details_by_not_authorized_user(self):
        with allure.step("Get user data for unauthorized user"):
            response_get = MyRequests.get(uri="/user/2")

        with allure.step("Check that status code = 200 and field 'username' exists in the response"):
            Assertions.assert_status_code(response=response_get, expected_status_code=200)
            Assertions.assert_json_has_key(response=response_get, name="username")

        with allure.step("Check that there are no other fields in the response"):
            not_expected_fields = ["id", "email", "firstName", "lastName"]
            Assertions.assert_json_has_no_keys(response=response_get, names=not_expected_fields)

    @allure.description("Test checks that user details contains the whole information for authorized request")
    def test_get_details_by_current_authorized_user(self):
        self.login(email="vinkotov@example.com", password="1234")

        response_get = self.get_user_info(user_id=self.user_id)

        with allure.step("Check that status code = 200 and all required fields exist in the response"):
            Assertions.assert_status_code(response=response_get, expected_status_code=200)

            expected_fields = ["id", "username", "email", "firstName", "lastName"]
            Assertions.assert_json_has_keys(response=response_get, names=expected_fields)

    @allure.description("Test checks that user details contains only username for another user")
    def test_get_details_by_another_authorized_user(self):
        self.login(email="vinkotov@example.com", password="1234")

        response_get = self.get_user_info(1)  # another user id

        with allure.step("Check that status code = 200 and field 'username' exists in the response"):
            Assertions.assert_status_code(response=response_get, expected_status_code=200)
            Assertions.assert_json_has_key(response=response_get, name="username")

        with allure.step("Check that there are no other fields in the response"):
            not_expected_fields = ["id", "email", "firstName", "lastName"]
            Assertions.assert_json_has_no_keys(response=response_get, names=not_expected_fields)
