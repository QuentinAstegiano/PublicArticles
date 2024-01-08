# Writing unit tests in Python

## An example

## Pre requisites

* python > 3.7
* pytest : https://docs.pytest.org/

Recommendation : using venv

Installing with pip : 
> $ pip install pytest

Checking install : 
> $ pytest --version
> pytest 7.4.4

## Organizing your tests

tests methods must be prefixed by test_
Separate test from source code : each should be in a separate folder hierarchy
Use Classes to group test (on a technical or functional scope)
Classes must be prefixed by Test

Use a naming convention and be consistent
For example : 
> test_[method name]_should_[X]_when_[y]

It makes for long names, but remember, the reading is important, not the writing

## Writing your tests

Some very simple tests : sources/test/test_adder.py
Using assert to validate the behavior of the methods
Using pytest.raises to check for expected exceptions

## Executing your tests

Calling pytest
