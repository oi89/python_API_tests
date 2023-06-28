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
