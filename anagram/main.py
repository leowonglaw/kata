from itertools import permutations


def get_anagrams(word: str):
    a = permutations(word, len(word))
    return [''.join(x) for x in a]
