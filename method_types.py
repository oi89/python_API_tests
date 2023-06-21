import requests


response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response.text)  # Wrong method provided

payload = {"method": "HEAD"}
response = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type", params=payload)
print(response.text)  # "" (empty response)

payload = {"method": "GET"}
response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params=payload)
print(response.text)  # {"success":"!"}

method_types = ["GET", "POST", "PUT", "DELETE"]
for method in method_types:
    response_get = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": method})
    response_post = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": method})
    response_put = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": method})
    response_delete = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": method})

    if method != "GET" and response_get.text == '{"success":"!"}':
        print(f"method=GET, parameter={method}: {response_get.text}")
    if method != "POST" and response_post.text == '{"success":"!"}':
        print(f"method=POST, parameter={method}: {response_post.text}")
    if method != "PUT" and response_put.text == '{"success":"!"}':
        print(f"method=PUT, parameter={method}: {response_put.text}")
    if method != "DELETE" and response_delete.text == '{"success":"!"}':
        print(f"method=DELETE, parameter={method}: {response_delete.text}")  # method=DELETE, parameter=GET: {"success":"!"}
