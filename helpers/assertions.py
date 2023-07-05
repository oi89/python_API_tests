from requests import Response
from json.decoder import JSONDecodeError


class Assertions:
    @staticmethod
    def get_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            json_dict = response.json()
        except JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in json_dict, f"Response JSON doesn't have the key '{name}'"
        assert json_dict[name] == expected_value, error_message

    @staticmethod
    def assert_status_code(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, \
            f"Unexpected status code. Expected: {expected_status_code}. Actual: {response.status_code}"

    @staticmethod
    def assert_json_has_key(response: Response, name):
        try:
            json_dict = response.json()
        except JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in json_dict, f"Response JSON doesn't have the key '{name}'"

    @staticmethod
    def assert_response_text(response: Response, expected_text):
        assert response.text == expected_text, f"Unexpected response. Expected: {expected_text}. Actual: {response.text}"
