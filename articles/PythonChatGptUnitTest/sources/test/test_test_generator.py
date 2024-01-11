import pytest
from main.test_generator import TestGenerator


class TestTestGenerator:
    @pytest.fixture
    def generator(self) -> TestGenerator:
        return TestGenerator()

    def test_test_generator_should_read_a_file_content(self, generator: TestGenerator):
        assert generator.get_file_content("sources/main/calculator.py") == "hmm"
