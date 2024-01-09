import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
print(sys.path)

from examples.increment import increment

def test_increment_should_add_one():
  assert increment(5) == 6
