# Writing unit tests in Python

Here you'll learn how to create some tests in python using pytest.

## An example

> def increment(x : int) -> int :
>   return add(x, 1)

> def test_increment_should_add_one(self):
>   assert adder.increment(5) == 6

> $ pytest sources/test/test_increment.py
> =================================== test session starts ===================================
> platform linux -- Python 3.11.6, pytest-7.4.0, pluggy-1.2.0
> rootdir: /home/quentin/workspace/articles/articles/PythonUnitTest
> collected 1 item
> 
> sources/test/test_increment.py .                                                    [100%]
> 
> ==================================== 1 passed in 0.00s ====================================

## Pre requisites

* python > 3.7
* pytest : https://docs.pytest.org/

I recommend using *venv* for managing your dependencies.
Not sure why or how ? [Check my article on the subject.](https://medium.com/@quentin.astegiano/effective-python-development-harnessing-the-power-of-virtual-environments-c01308189d6c)

*pytest* is best installed with pip : 
> $ pip install pytest

Check your install with the following command :
> $ pytest --version
> pytest 7.4.4

## Organizing your tests

### Method naming

All *pytest* test method must be prefixed by *"test_"*
You should pick a naming pattern for your tests and stick to it.

I recommend the following : 
> test_[method]_should_[aspect of method tested]
It makes for long names, but remember, the reading is what is important, not the writing.

For example : 
> def test_increment_should_add_one():
> def test_is_prime_should_validate_prime_number():

### Tests location

I strongly recommend to separate your tests from your source code. Each should be in a separate folder hierarchy.
For example :
> sound_manager
>   main
>     formats
>       wavread.py
>       auwrite.py
>     effect
>       echo.py
>       surround.py
>     filters
>       equalizer.py
>   test 
>     formats
>       test_wavread.py
>       test_auwrite.py
>     effects
>       test_echo.py
>       test_surround.py
>     filters
>       test_equalizer.py

If you don't know how to manage folder hierarchy in python, or how to call a method from another folder, check out my other article where I explain all about __init__.py 

### Using classes

You should use classes to group your tests, either on a technical or a functional scope. 
Test classes must be named with the prefix *Test*.

For example : 
> class TestIncrement: 
>   def test_increment_should_add_one(self):
>     assert adder.increment(5) == 6
> 
>   def test_increment_should_work_with_negatives(self):
>     assert adder.increment(-5) == -4
> 
>   def test_increment_should_not_accept_none(self):
>     with pytest.raises(TypeError):
>       a = None
>       adder.increment(a)

## Writing your tests

Some very simple tests : sources/test/test_adder.py
Using assert to validate the behavior of the methods
Using pytest.raises to check for expected exceptions

## Executing your tests

Calling pytest
