def is_prime(number: int):
    count = 2
    if number < count:
        return False
    while count < number:
        if number % count == 0:
            return False
        count += 1
    return True
