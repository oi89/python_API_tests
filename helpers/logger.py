import os
from datetime import datetime
from requests import Response


class Logger:
    file_name = f"logs/log{datetime.now().strftime('%d-%m-%Y-_%H-%M-%S')}.log"

    @classmethod
    def _write_to_file(cls, data: str):
        with open(file=cls.file_name, mode="a", encoding="utf-8") as log_file:
            log_file.write(data)

    @classmethod
    def add_request(cls, url: str, data: dict, cookies: dict, headers: dict, method: str):
        test_name = os.environ.get("PYTEST_CURRENT_TEST")

        data_to_add = "\n-----\n"
        data_to_add += f"Test: {test_name}\n"
        data_to_add += f"Time: {str(datetime.now())}\n"
        data_to_add += f"Request method: {method}\n"
        data_to_add += f"Request URL: {url}\n"
        data_to_add += f"Request data: {data}\n"
        data_to_add += f"Request headers: {headers}\n"
        data_to_add += f"Request cookies: {cookies}\n"
        data_to_add += "\n"

        cls._write_to_file(data=data_to_add)

    @classmethod
    def add_response(cls, response: Response):
        cookies_as_dict = dict(response.cookies)
        headers_as_dict = dict(response.headers)

        data_to_add = f"Response code: {response.status_code}\n"
        data_to_add += f"Response test: {response.text}\n"
        data_to_add += f"Response headers: {headers_as_dict}\n"
        data_to_add += f"Response cookies: {cookies_as_dict}\n"
        data_to_add += "-----\n"

        cls._write_to_file(data=data_to_add)
