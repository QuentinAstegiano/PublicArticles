from main.lib.util_lib import multiply_by_two
import pytest


class TestMultiply:
    def test_multiply_by_two_should_double_input(self):
        assert multiply_by_two(5) == 10

    @pytest.mark.skip("Remote data not available")
    def test_multiply_by_two_should_do_something_with_an_external_call(self):
        remote_data = import_remote_data()
        assert multiply_by_two(remote_data[0]) == remote_data[1]
