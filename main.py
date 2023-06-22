import requests
from json.decoder import JSONDecodeError


payload = {"name": "User"}
response = requests.get("https://playground.learnqa.ru/api/hello", params=payload)
json_obj = response.json()  # {'answer': 'Hello, User'}
print(json_obj["answer"])


response = requests.get("https://playground.learnqa.ru/api/get_text")
try:
    json_obj = response.json()
    print(json_obj)
except JSONDecodeError:
    print("Incorrect json format")


response = requests.get("https://playground.learnqa.ru/api/check_type", params={"param1": "value1"})
print(response.text)
response = requests.post("https://playground.learnqa.ru/api/check_type", data={"param2": "value2"})
print(response.text)


response = requests.get("https://playground.learnqa.ru/api/get_301", allow_redirects=True)
first_response = response.history[0]
second_response = response
print(f"{first_response.status_code}: {first_response.url}")
print(f"{second_response.status_code}: {second_response.url}")


headers = {"header1": "some value 1"}
response = requests.get("https://playground.learnqa.ru/api/show_all_headers", headers=headers)
print(response.text)  # request headers
print(response.headers)  # response headers


payload = {"login": "secret_login", "password": "secret_pass"}
response = requests.post("https://playground.learnqa.ru/api/get_auth_cookie", data=payload)
print(dict(response.cookies))
cookie_value = response.cookies.get("auth_cookie")

cookies = {}
if cookie_value is not None:
    cookies.update({"auth_cookie": cookie_value})  # add value to dictionary

response2 = requests.post("https://playground.learnqa.ru/api/check_auth_cookie", cookies=cookies)
print(response2.text)
