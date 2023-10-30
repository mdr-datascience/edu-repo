# Import pytest
import pytest

# Check if pytest runs
def test_canRunPyTest():
    assert True

# Function for first exercise in the tutorial
def sayHelloWorld(value):
    if value == 1:
        return "hello"
    if value == 2:
        return "world"

# First test case
def test_canCallSayHelloWorld():
    sayHelloWorld(1)

# Second test case
def test_returnsHelloWhenInputIs1():
     retVal = sayHelloWorld(1)
     assert retVal == "hello"

# Third test case
def test_returnsHelloWhenInputIs2():
    retVal = sayHelloWorld(2)
    assert retVal == "world"

# Function to refactor code
def checkSayHelloWorld(value, expOut):
    retVal = sayHelloWorld(value)
    assert retVal == expOut

# Refactored first test
def test_returnsHelloWhenInputIs1_refactored():
     checkSayHelloWorld(1,"hello")

# Refactored second test
def test_returnsHelloWhenInputIs2_refactored():
    checkSayHelloWorld(2, "world")

# Function to demonstrate approx functionality
def divide(a, b):
    return a / b

# Test case without approx functionality
def test_exact_comparison():
    result = divide(1, 3)
    assert result == 0.3333333333333333

# Test case with approx functionality
def test_approximate_comparison():
    result = divide(1, 3)
    assert result == pytest.approx(0.3333333)

# Function to demonstrate with raises functionality
def myFunction(x):
    if x > 10:
        raise ValueError

# Test exception
def test_exceptionFunction():
    with pytest.raises(ValueError):
        myFunction(100)

# Function to test ZeroDivisionError exception
def divideTwoNumbers(a, b):
    if b != 0:
        val = a/b
        return val
    else:
        raise ZeroDivisionError

# Test for ZeroDivisionError exeception
def test_divisionErrorFunction():
    with pytest.raises(ZeroDivisionError):
        divideTwoNumbers(10, 0)
