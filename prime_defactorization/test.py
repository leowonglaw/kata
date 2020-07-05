import unittest
from main import defactor


class TestPrimeDefactorization(unittest.TestCase):
    ''' Based on https://www.youtube.com/watch?v=kScFczWbwRM&t=1086s '''

    def test_defactor_of_one_is_one(self):
        result = defactor(1)
        self.assertEqual(result, [])

    def test_defactor_of_two_is_two(self):
        result = defactor(2)
        self.assertEqual(result, [2])

    def test_defactor_of_three_is_three(self):
        result = defactor(3)
        self.assertEqual(result, [3])

    def test_defactor_of_four_is_two_two(self):
        result = defactor(4)
        self.assertEqual(result, [2, 2])

    def test_defactor_of_five_is_five(self):
        result = defactor(5)
        self.assertEqual(result, [5])

    def test_defactor_of_six_is_two_three(self):
        result = defactor(6)
        self.assertEqual(result, [2, 3])

    def test_defactor_of_seven_is_seven(self):
        result = defactor(7)
        self.assertEqual(result, [7])

    def test_defactor_of_eigth_is_two_two_two(self):
        result = defactor(8)
        self.assertEqual(result, [2, 2, 2])

    def test_defactor_of_nine_is_three_three(self):
        result = defactor(9)
        self.assertEqual(result, [3, 3])

    def test_defactor_of_long_number(self):
        result = defactor(2*2*3*5*7*11*11)
        self.assertEqual(result, [2, 2, 3, 5, 7, 11, 11])


if __name__ == "__main__":
    unittest.main()
