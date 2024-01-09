import examples.adder as adder
import pytest

class TestIncrement: 
  def test_increment_should_add_one(self):
    assert adder.increment(5) == 6

  def test_increment_should_work_with_negatives(self):
    assert adder.increment(-5) == -4

  def test_increment_should_not_accept_none(self):
    with pytest.raises(TypeError):
      a = None
      adder.increment(a)

class TestAdd:
  def test_add_should_add_specified_value(self):
    assert adder.add(3, 4) == 7

  def test_addd_should_work_with_negatives(self):
    assert adder.add(-5, 6) == 1
