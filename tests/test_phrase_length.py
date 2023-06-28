def test_phrase_length():
    phrase = input("Set a phrase: ")

    assert len(phrase) < 15, "Length of the phrase in not less than 15 symbols"
