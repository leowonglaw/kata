import unittest
from main import get_anagrams

'''
https://www.codeproject.com/Articles/498404/TDD-the-Anagrams-Kata
Write a program to generate all potential anagrams of an input string. 
For example, the potential anagrams of "biro" are 
biro bior brio broi boir bori 
ibro ibor irbo irob iobr iorb 
rbio rboi ribo riob roib robi 
obir obri oibr oirb orbi orib
'''

class TestAnagram(unittest.TestCase):

    def test_one_letter(self):
        anagrams = get_anagrams('A')
        self.assertIn('A', anagrams)

    def test_two_letters(self):
        anagrams = get_anagrams('AB')
        self.assertIn('AB', anagrams)
        self.assertIn('BA', anagrams)

    def test_three_letters(self):
        anagrams = get_anagrams('ABC')
        self.assertIn('ABC', anagrams)
        self.assertIn('CBA', anagrams)
        self.assertIn('BCA', anagrams)
        self.assertIn('BAC', anagrams)

if __name__ == '__main__':
    unittest.main()
