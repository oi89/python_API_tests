class TestExample:

    def test_pass(self):
        a = 1
        b = 2
        expected_sum = 3

        assert a + b == expected_sum, f"Sum of a and b not equal to {expected_sum}"

    def test_fail(self):
        a = 1
        b = 0
        expected_sum = 3

        assert a + b == expected_sum, f"Sum of a and b not equal to {expected_sum}"

