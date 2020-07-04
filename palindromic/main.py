import math

def is_palindromic(number: int):
    reverse_number = 0
    numeral = number
    while numeral:
        res = numeral % 10
        reverse_number = reverse_number*10 + res
        numeral //= 10
    return number == reverse_number
