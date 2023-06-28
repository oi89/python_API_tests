import requests
import pytest


class TestFirstAPI:

    names = ["Tom", "Tom White", ""]

    @pytest.mark.parametrize("name", names)
    def test_hello_call(self, name):
        url = "https://playground.learnqa.ru/api/hello"

        data = {"name": name}
        response = requests.get(url=url, params=data)

        assert response.status_code == 200, "Incorrect status code in the response"

        response_dist = response.json()

        assert "answer" in response_dist, "There is no field 'answer' in the response"

        actual_response_text = response_dist["answer"]
        if len(name) == 0:
            expected_response_text = "Hello, someone"
        else:
            expected_response_text = f"Hello, {name}"

        assert actual_response_text == expected_response_text, "Actual response text isn't correct"

