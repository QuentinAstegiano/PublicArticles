import pytest

@pytest.fixture
def calculator():
    return Calculator()

def test_add(calculator):
    assert calculator.add(2) == 2
    assert calculator.add(3) == 5

def test_sub(calculator):
    assert calculator.sub(1) == -1
    assert calculator.sub(3) == -4

def test_mult(calculator):
    assert calculator.mult(2) == 0
    assert calculator.mult(3) == 0

def test_div(calculator):
    assert calculator.div(2) == 0
    assert calculator.div(3) == 0