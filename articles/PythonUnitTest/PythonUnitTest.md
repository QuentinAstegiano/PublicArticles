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
> main 
>   lib
>     util_lib.py 
>   adder.py 
>   increment.py 
> test 
>   lib 
>     __init__.py
>     test_util_lib.py 
>   __init__.py
>   test_adder.py 
>   test_increment.py

To be able to access modules from another folder, you'll need to edit the sys.path of python to tell it where to look.
The easiest way I found for that is simply to set *__init__.py* files in your test folders ; and to set the following code in the one in the test parent folder : 
    
> import sys
> import os
> 
> def find_specific_parent(pattern, current = None):
>     if current is None:
>         return find_specific_parent(pattern, os.path.dirname(__file__))
>     else:
>         splitted = current.split(os.sep)
>         if pattern == splitted[-1]:
>             return current
>         else:
>             if len(splitted) == 1:
>                 return None
>             else:
>                 return find_specific_parent(pattern, os.sep.join(splitted[0:-1]))
> 
>     
> def get_parent_sibling(parent, sibling_name):
>     parent = find_specific_parent(parent)
>     return os.sep.join([os.path.dirname(parent), sibling_name])
> 
> sys.path.append(get_parent_sibling("test", "main"))

This code will add the *main* folder (where all the source code reside) to all test files, allowing them to easily include the main modules : 

> from main.increment import increment
> 
> def test_increment_should_add_one():
>   assert increment(5) == 6

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

Writing test with *pytest* is very easy. Call your method, use *assert* to validate their result, and voilà, you've got a test !
In addition to the very simple examples already listed earlier, here's some useful things you can do with *pytest*

### Checking expected exceptions

If you have code that is expected to raise an exception given, for example, a certain parameter, then you can test for that with *pytest*
For example, given a code that execute a division : 

> def int_divide(numerator: int, denominator: int) -> int :
>   if denominator == 0:
>     raise TypeError("denominator should not be 0")
>   return numerator // denominator

You can easily test that this error is raised with the following syntax :

> def test_int_division_should_raise_error_when_denominator_is_zero(self):
>   with pytest.raises(TypeError):
>     int_divide(5, 0)


### Marking tests

*Marks* are another powerful feature of *pytest*. They'll allow you to tag your test, either with builtins marks, or with custom ones.
Using them is easy : just annotate the test method.

Some useful marks are : 

* Skip : ignore the test

>  @pytest.mark.skip("Remote data not available")
>  def test_multiply_by_two_should_do_something_with_an_external_call(self):
>    remote_data = import_remote_data()
>    assert multiply_by_two(remote_data[0]) == remote_data[1]

A very powerful aspect of that mark is that this code is not executed at all ; it can even contains broken code, like, here, a reference to a function that doesn't exist.

* XFail : a test that is expected to fail

Sometimes when you write a test, you know that it is going to fail. 
It should not fail, this is only temporary, but right now, it'll - maybe because it depend on some external broken service, maybe because some part of the implentation is not done yet.

In that case, the *@pytest.mark.xfail* will allow you to mark that test, to insure that it's failure is not reported as a whole test failure.

Please note that *xfail* should not be used for test that should be failing all the times ; use *assert not* in that case.

* Custom marks

To register your custom marks, you need to specify them in a *pytest.ini* file.
I recommend to put that file in the root folder of your test, and to reference it when you execute pytest.

For exemple the given configuration create a "slow" mark : 

> [pytest]
> markers = 
>   slow : mark slow tests

That mark can be then be used in your tests like the builtins ones : 

>  @pytest.mark.slow
>  def test_int_division_should_produce_good_results_everytime(self):
>    for i in range(1, 1000):
>      for j in range(1, 1000):
>        assert int_divide(i, j) == i // j

One use of those marks is to execute tests based on their mark, for exemple 

> pytest -k "not slow"
> pytest -k "smoke_test"
> pytest -k "slow or http"

This is extremely useful when defining CI jobs, when you want to have a specific job the integrations tests ; or if you want to run some quick tests in a pre-commit git hook.

### Test parametrization

### Fixtures

## Executing your tests

That's also quite easy : just call *pytest* from your folder.
*pytest* take many optional parameters ; here's some that I found quite useful :

To specify a config file :

> pytest -c tests/pytest.ini

To execute only some tests, based on marks or test method name :

> pytest -k "smoke_test"
> pytest -k "test_multiply"

To print the durations of the slower tests :

> pytest --durations=0
