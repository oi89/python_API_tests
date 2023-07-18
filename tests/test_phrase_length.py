import allure
import pytest


@allure.epic("String length")
class TestPhraseLength:

    @pytest.mark.xfail(condition=lambda: True, reason="Expected failure with no input string")
    @allure.description("Test checks a length of input string")
    def test_phrase_length(self):
        with allure.step("Receive a input string"):
            phrase = input("Set a phrase: ")

        with allure.step("Check that the length of a string is less than 15 symbols"):
            assert len(phrase) < 15, "Length of the phrase in not less than 15 symbols"
