import requests
import allure

from helpers.logger import Logger
from environment import ENV_OBJECT


class MyRequests:

    @staticmethod
    def get(uri: str, data: dict = None, cookies: dict = None, headers: dict = None):
        with allure.step(f"GET request to URL {uri}"):
            return MyRequests._send(uri=uri, data=data, cookies=cookies, headers=headers, method="GET")

    @staticmethod
    def post(uri: str, data: dict = None, cookies: dict = None, headers: dict = None):
        with allure.step(f"POST request to URL {uri}"):
            return MyRequests._send(uri=uri, data=data, cookies=cookies, headers=headers, method="POST")

    @staticmethod
    def put(uri: str, data: dict = None, cookies: dict = None, headers: dict = None):
        with allure.step(f"PUT request to URL {uri}"):
            return MyRequests._send(uri=uri, data=data, cookies=cookies, headers=headers, method="PUT")

    @staticmethod
    def delete(uri: str, data: dict = None, cookies: dict = None, headers: dict = None):
        with allure.step(f"DELETE request to URL {uri}"):
            return MyRequests._send(uri=uri, data=data, cookies=cookies, headers=headers, method="DELETE")

    @staticmethod
    def _send(uri: str, data: dict, cookies: dict, headers: dict, method: str):
        url = f"{ENV_OBJECT.get_base_url()}{uri}"

        if data is None:
            data = {}
        if cookies is None:
            cookies = {}
        if headers is None:
            headers = {}

        Logger.add_request(url=url, data=data, cookies=cookies, headers=headers, method=method)

        if method == "GET":
            response = requests.get(url=url, params=data, cookies=cookies, headers=headers)
        if method == "POST":
            response = requests.post(url=url, data=data, cookies=cookies, headers=headers)
        if method == "PUT":
            response = requests.put(url=url, data=data, cookies=cookies, headers=headers)
        if method == "DELETE":
            response = requests.delete(url=url, data=data, cookies=cookies, headers=headers)

        Logger.add_response(response=response)

        return response
