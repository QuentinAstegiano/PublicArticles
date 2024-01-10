import pytest
from main.my_math import int_divide

class TestIntDivision:

    def test_int_division_should_divide_numerator_by_denominator(self):
        assert int_divide(10, 2) == 5

    def test_int_division_should_not_produce_incorrect_results(self):
        assert not int_divide(10, 2) == 3

    def test_int_division_should_raise_error_when_denominator_is_zero(self):
        with pytest.raises(TypeError):
            int_divide(5, 0)

    @pytest.mark.slow
    def test_int_division_should_produce_good_results_everytime(self):
        for i in range(1, 1000):
            for j in range(1, 1000):
                assert int_divide(i, j) == i // j
