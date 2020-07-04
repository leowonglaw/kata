import unittest
from main import is_prime


class TestPrimeNumber(unittest.TestCase):
    
    def test_one_is_not_prime(self):
        result = is_prime(1)
        self.assertEqual(result, False)

    def test_short_primes(self):
        some_primes = [2, 3, 5, 7, 11, 13]
        for num in some_primes:
            self.assertEqual(is_prime(num), True, num)

    def test_short_not_primes(self):
        some_not_primes = [1, 4, 6, 8, 9, 10, 12, 14]
        for num in some_not_primes:
            self.assertEqual(is_prime(num), False, num)

    def test_multiples_of_two(self):
        some_not_primes = [4, 6, 8, 10, 1000, 46]
        for num in some_not_primes:
            self.assertEqual(is_prime(num), False, num)

    def test_multiples_of_three(self):
        some_not_primes = [6, 9, 12, 15, 30]
        for num in some_not_primes:
            self.assertEqual(is_prime(num), False, num)

    def test_long_primes(self):
        some_primes = [97, 19, 17, 197, 199]
        for num in some_primes:
            self.assertEqual(is_prime(num), True, num)

    def test_long_not_primes(self):
        some_not_primes = [152, 153, 155, 7*7, 97*97]
        for num in some_not_primes:
            self.assertEqual(is_prime(num), False, num)


if __name__ == "__main__":
    unittest.main()
