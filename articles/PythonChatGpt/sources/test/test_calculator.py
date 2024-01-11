from main.calculator import ChatGptCalculator
import pytest


class TestChatGptCalculator:
    @pytest.fixture
    def calculator(self) -> ChatGptCalculator:
        return ChatGptCalculator()

    def test_calculator_should_do_additions(self, calculator: ChatGptCalculator):
        assert calculator.calculate("3+5") == 8.0

    def test_calculator_should_do_substractions(self, calculator: ChatGptCalculator):
        assert calculator.calculate("12 - 3") == 9.0

    def test_calculator_should_do_multiplications(self, calculator: ChatGptCalculator):
        assert calculator.calculate("8 * 4") == 32.0
