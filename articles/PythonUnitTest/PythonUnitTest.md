# Simple and Easy Unit Testing in Python with Pytest

In this guide, you'll learn how to create tests in Python using Pytest.

## An Example

```python
def increment(x: int) -> int:
    return add(x, 1)
def test_increment_should_add_one():
    assert increment(5) == 6
```

```bash
$ pytest sources/test/test_increment.py
```

You can find all source code presented here on my [GitHub](https://github.com/QuentinAstegiano/PublicArticles/tree/main/articles/PythonUnitTest/sources)

## Prerequisites

* Python > 3.7
* Pytest: [https://docs.pytest.org/](https://docs.pytest.org/)

I recommend using *venv* for managing your dependencies. If you're unsure how, check [my article on the subject](https://medium.com/@quentin.astegiano/effective-python-development-harnessing-the-power-of-virtual-environments-c01308189d6c).

Install *pytest* with:

```bash
$ pip install pytest
```

Check your install:

```bash
$ pytest --version
pytest 7.4.4
```

## Organizing Your Tests

### Method Naming

All *pytest* test methods must be prefixed by *"test_"*. Use a consistent naming pattern for your tests. For example:

```python
def test_increment_should_add_one():
def test_is_prime_should_validate_prime_number():
```

I recommend a pattern like *test_[method]_should_[method use case]*.
Those names tend to be long, but it'll be easier to understand - the reading matter more than the writing. 

### Tests Location

Separate your tests from your source code. Each should be in a separate folder hierarchy. For example:

```
main
  lib
    util_lib.py
  adder.py
  increment.py
test
  lib
    __init__.py
    test_util_lib.py
  __init__.py
  test_adder.py
  test_increment.py
```

To access modules from another folder, set *__init__.py* files in your test folders to declare them as modules, and use the following code in the test parent folder:

```python
import sys
import os

def find_specific_parent(pattern, current = None):
  if current is None:
    return find_specific_parent(pattern, os.path.dirname(__file__))
  else:
    splitted = current.split(os.sep)
    if pattern == splitted[-1]:
      return current
    else:
      if len(splitted) == 1:
        return None
      else:
        return find_specific_parent(pattern, os.sep.join(splitted[0:-1]))
  
def get_parent_sibling(parent, sibling_name):
  parent = find_specific_parent(parent)
  return os.sep.join([os.path.dirname(parent), sibling_name])

sys.path.append(get_parent_sibling("test", "main"))
```

This code adds the *main* folder to the sys path of all test files, allowing them to include the main modules:

```python
from main.increment import increment

def test_increment_should_add_one():
    assert increment(5) == 6
```

### Using Classes

Group your tests using classes, either on a technical or functional scope. Test classes must be named with the prefix *Test*. For example:

```python
class TestIncrement:
  def test_increment_should_add_one(self):
    assert increment(5) == 6

  def test_increment_should_work_with_negatives(self):
    assert increment(-5) == -4

  def test_increment_should_not_accept_none(self):
    with pytest.raises(TypeError):
      a = None
      increment(a)
```

## Writing Your Tests

Writing tests with *pytest* is straightforward. Call your method, use *assert* to validate their result, and voilà, you've got a test! In addition to the simple examples listed earlier, here are some useful things you can do with *pytest*.

### Checking Expected Exceptions

If your code is expected to raise an exception under certain conditions, use *pytest*. For example:

```python
def int_divide(numerator: int, denominator: int) -> int:
  if denominator == 0:
    raise TypeError("denominator should not be 0")
  return numerator // denominator

def test_int_division_should_raise_error_when_denominator_is_zero():
  with pytest.raises(TypeError):
    int_divide(5, 0)
```

### Marking Tests

Use *marks* to tag your tests with built-in or custom marks. Annotate the test method accordingly. Useful marks include:

* Skip: Ignore the test

```python
@pytest.mark.skip("Remote data not available")
def test_multiply_by_two_should_do_something_with_an_external_call():
  remote_data = import_remote_data()
  assert multiply_by_two(remote_data[0]) == remote_data[1]
```

A very powerful aspect of that mark is that this code is not executed at all ; it can even contains broken code, like, here, a reference to a function that doesn't exist.

* XFail: Mark a test as expected to fail temporarily

```python
@pytest.mark.xfail
def test_some_temporary_failure():
    # ...
```

Sometimes when you write a test, you know that it is going to fail. It should not fail, this is only temporary, but right now, it'll - maybe because it depend on some external broken service, maybe because some part of the implentation is not done yet.

In that case, the @pytest.mark.xfail will allow you to mark that test, to insure that it's failure is not reported as a whole test failure.

Please note that xfail should not be used for test that should be failing all the times ; use *assert not* in that case.

* Custom Marks: Register custom marks in *pytest.ini*

```ini
[pytest]
markers = 
  slow: mark slow tests
```

Use the custom mark in your tests:

```python
@pytest.mark.slow
def test_int_division_should_produce_good_results_everytime():
  for i in range(1, 1000):
    for j in range(1, 1000):
      assert int_divide(i, j) == i // j
```

One use of these marks is to execute tests based on their tags, for example:

```bash
pytest -k "not slow"
pytest -k "smoke_test"
pytest -k "slow or http"
```

This is extremely useful when defining CI jobs, when you want to have a specific job the integrations tests ; or if you want to run some quick tests in a pre-commit git hook.

### Test Parametrization

Parametrize tests with *@pytest.mark.parametrize* to execute the same test with different parameters, avoiding code repetition. For example:

```python
class TestIsPrime:
    @pytest.mark.parametrize("number, prime_status", [(2, True), (3, True), (4, False), (5, True)])
    def test_is_prime_should_recognize_prime_numbers(self, number, prime_status):
        assert is_prime(number) == prime_status
```

The annotation take a first argument describing the various parameter that this method will use ; and a list of tuples, each containing a value for each parameter defined in the first argument. For example here, the is_prime method is going to check that 2 and 3 are indeed primes number, that 4 is not, etc.

### Fixtures

Fixtures are powerful and advanced features of *pytest*. They allow you to execute a function once and cache its result for multiple test methods. For example:

```python
from dataclasses import dataclass

@dataclass
class Person:
  age: int
  first_name: str
  last_name: str

def is_person_older(person : Person, than : int) -> bool:
  return person.age > than
```

```python
class TestIsPersonOlder:
  @pytest.fixture
  def some_person(self):
    return Person(15, "John", "Doe")

  def test_is_person_older_recognize_a_young_person(self, some_person):
    assert is_person_older(some_person, 5) is True

  def test_is_person_older_recognize_an_old_person(self, some_person):
    assert is_person_older(some_person, 95) is False
```

Here, by declaring some_person as a fixture, I can use it as a parameter in my tests methods. It's result is captured and provided. That's nice : but the real beauty of it is that fixture are only executed once, and its result is cached.

That mean that you can hide some expensive data behind fixture (something from a database or a remote call) ; or you can provide with a fixture something that should be instanciated only once, like a cache, a connection to a webservice, something that contains an intrinsic random part (like an UID), ...

## Executing Your Tests

Execute your tests by calling *pytest* from your folder. Some useful parameters include:

Specify a config file:

```bash
pytest -c tests/pytest.ini
```

Execute only specific tests based on marks or test method names:

```bash
pytest -k "smoke_test"
pytest -k "test_multiply"
```

Print the durations of the slower tests:

```bash
pytest --durations=0
```
