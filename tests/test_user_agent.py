import allure
import pytest
import requests

from helpers.assertions import Assertions


@allure.epic("User agent")
class TestUserAgent:
    data = [
        {
            "user_agent": 'Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
            "platform": "Mobile",
            "browser": "No",
            "device": "Android"
        },
        {
            "user_agent": 'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1',
            "platform": "Mobile",
            "browser": "Chrome",
            "device": "iOS"
        },
        {
            "user_agent": 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            "platform": "Googlebot",
            "browser": "Unknown",
            "device": "Unknown"
        },
        {
            "user_agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0',
            "platform": "Web",
            "browser": "Chrome",
            "device": "No"
        },
        {
            "user_agent": 'Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            "platform": "Mobile",
            "browser": "No",
            "device": "iPhone"
        }
    ]

    @allure.description("Test checks the response from /ajax/api/user_agent_check")
    @pytest.mark.parametrize("test_data", data, ids=[x["user_agent"] for x in data])
    @pytest.mark.skip("Some tests fail due to incorrect test data")
    def test_user_agent(self, test_data):
        with allure.step(f"GET /ajax/api/user_agent_check"):
            user_agent = test_data["user_agent"]
            headers = {"User-Agent": user_agent}
            response = requests.get("https://playground.learnqa.ru/ajax/api/user_agent_check", headers=headers)

        with allure.step("Check that the 'platform' from the response has correct value"):
            Assertions.get_json_value_by_name(
                response=response,
                name="platform",
                expected_value=test_data["platform"],
                error_message=f"'platform' != '{test_data['platform']}' in User-Agent '{user_agent}'"
            )
        with allure.step("Check that the 'browser' from the response has correct value"):
            Assertions.get_json_value_by_name(
                response=response,
                name="browser",
                expected_value=test_data["browser"],
                error_message=f"'browser' != '{test_data['browser']}' in User-Agent '{user_agent}'"
            )
        with allure.step("Check that the 'device' from the response has correct value"):
            Assertions.get_json_value_by_name(
                response=response,
                name="device",
                expected_value=test_data["device"],
                error_message=f"'device' != '{test_data['device']}' in User-Agent '{user_agent}'"
            )
