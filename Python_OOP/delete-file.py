def scope_test():
    def do_local():
        spam = "local spam"

    def do_nonlocal():
        nonlocal spam
        spam = "nonlocal spam"

    def do_global():
        global spam
        spam = "global spam"

    spam = "test spam"
    do_local()
    print("After local assignment:", spam)
    do_nonlocal()
    print("After nonlocal assignment:", spam)
    do_global()
    print("After global assignment:", spam)

scope_test()
print("In global scope:", spam)

class MyClass:
    """A simple example class"""
    i = 12345

    def f(self):
        return 'hello world'
    
obj = MyClass()
print(obj.i)
print(obj.f)
print(obj.__doc__)

class MyNumbers:
  def __iter__(self):
    self.a = 1
    return self

  def __next__(self):
    self.a += 10
    return self.a
  

myclass = MyNumbers()
myiter = iter(myclass)

print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))

def myfunc(val1,val2):
     ret_val = val1 ** val2
     return(ret_val)