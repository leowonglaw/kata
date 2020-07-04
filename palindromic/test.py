import unittest

from main import is_palindromic


class TestPalindromicNumber(unittest.TestCase):

    def test_numbers_lt_ten_are_palindomic(self):
        for num in range(1, 10):
            result = is_palindromic(num)
            self.assertEqual(result, True, num)

    def test_palindomic_lt_hundred(self):
        for num in range(1, 10):
            num *= 11
            result = is_palindromic(num)
            self.assertEqual(result, True, num)

    def test_not_palindomic_lt_hundred(self):
        numbers = [10, 23, 45, 90, 10, 50, 72]
        for num in numbers:
            result = is_palindromic(num)
            self.assertEqual(result, False, num)

    def test_palindomic_gte_hundred_lt_thousand(self):
        numbers = [101, 121, 333, 494, 212, 656, 707, 777]
        for num in numbers:
            result = is_palindromic(num)
            self.assertEqual(result, True, num)

    def test_not_palindomic_gte_hundred_lt_thousand(self):
        numbers = [100, 123, 145, 190, 110, 150, 720, 700]
        for num in numbers:
            result = is_palindromic(num)
            self.assertEqual(result, False, num)

    def test_palindomic_long_numbers(self):
        numbers = [123456654321, 8108018]
        for num in numbers:
            result = is_palindromic(num)
            self.assertEqual(result, True, num)

    def test_not_palindomic_long_numbers(self):
        numbers = [12346, 84562]
        for num in numbers:
            result = is_palindromic(num)
            self.assertEqual(result, False, num)


if __name__ == "__main__":
    unittest.main()
