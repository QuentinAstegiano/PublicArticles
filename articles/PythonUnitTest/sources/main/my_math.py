def int_divide(numerator: int, denominator: int) -> int :
    if denominator == 0:
        raise TypeError("denominator should not be 0")
    return numerator // denominator
