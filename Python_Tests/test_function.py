import pytest

def test_canRunPyTest():
    assert True

def sayHelloWorld(value):
    if value == 1:
        return "hello"
    if value == 2:
        return "world"

def test_canCallSayHelloWorld():
    sayHelloWorld(1)

def test_returnsHelloWhenInputIs1():
     retVal = sayHelloWorld(1)
     assert retVal == "hello"

def test_returnsHelloWhenInputIs2():
    retVal = sayHelloWorld(2)
    assert retVal == "world"

def checkSayHelloWorld(value, expOut):
    retVal = sayHelloWorld(value)
    assert retVal == expOut

def test_returnsHelloWhenInputIs1_refactored():
     checkSayHelloWorld(1,"hello")

def test_returnsHelloWhenInputIs2_refactored():
    checkSayHelloWorld(2, "world")

def divide(a, b):
    return a / b

def test_exact_comparison():
    result = divide(1, 3)
    assert result == 0.3333333333333333

def test_approximate_comparison():
    result = divide(1, 3)
    assert result == pytest.approx(0.3333333)

def raisesValueException():
    raise ValueError

def test_exceptionFunction():
    with pytest.raises(ValueError):
        raisesValueException()

def divideTwoNumbers(a, b):
    if b != 0:
        val = a/b
        return val
    else:
        raise ZeroDivisionError

def test_divisionErrorFunction():
    with pytest.raises(ZeroDivisionError):
        divideTwoNumbers(10, 0)
