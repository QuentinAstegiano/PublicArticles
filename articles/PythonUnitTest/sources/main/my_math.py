def int_divide(numerator: int, denominator: int) -> int:
    if denominator == 0:
        raise TypeError("denominator should not be 0")
    return numerator // denominator


def is_prime(number: int) -> bool:
    for i in range(2, number // 2 + 1):
        if number % i == 0:
            return False
    return True
