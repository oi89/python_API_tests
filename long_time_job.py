import requests
import time


url = "https://playground.learnqa.ru/ajax/api/longtime_job"

response = requests.get(url)
obj = response.json()
token = obj["token"]
delay_time = obj["seconds"]

payload = {"token": token}
response = requests.get(url, params=payload)
print(response.json()["status"])

print(f"Waiting {delay_time} seconds...")
time.sleep(delay_time)

response = requests.get(url, params=payload)
obj = response.json()
print(obj["status"])
if "result" in obj:
    print(obj["result"])
