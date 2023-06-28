from requests import Response
from json.decoder import JSONDecodeError


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
