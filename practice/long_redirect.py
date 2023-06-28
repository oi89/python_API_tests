import requests


response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)
print(f"Count of redirects: {len(response.history)}")  # 2
print(f"Final URL: {response.url}")  # https://learnqa.ru/
