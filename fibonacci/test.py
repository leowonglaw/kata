import unittest

from main import fibonacci

class TestFibonacci(unittest.TestCase):


    def test_one_number(self):
        fibo = fibonacci(1)
        self.assertEqual(fibo, [1])

    def test_two_numbers(self):
        fibo = fibonacci(2)
        self.assertEqual(fibo, [1, 2])

    def test_three_numbers(self):
        fibo = fibonacci(3)
        self.assertEqual(fibo, [1, 2, 3])

    def test_four_numbers(self):
        fibo = fibonacci(4)
        self.assertEqual(fibo, [1, 2, 3, 5])

    def test_five_numbers(self):
        fibo = fibonacci(5)
        self.assertEqual(fibo, [1, 2, 3, 5, 8])

if __name__ == "__main__":
    unittest.main()
