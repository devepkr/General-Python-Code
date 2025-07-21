import  logging
logging.basicConfig(level=logging.INFO)
def log_function_call(func):
    def decorated(*args, **kwargs):
        logging.info(f"calling {func.__name__} with args={args} kwargs={kwargs}")
        result = func(*args, **kwargs)
        logging.info(f"{func.__name__} returned {result}")
        return  result
    return decorated

@log_function_call
def my_function(a, b):
    return a + b
# my_function(10, 20)





"""

def my_decorators(func):
    def wrapper():
        print('Transaction  started')
        func()
        print('Transaction Completed')
    return wrapper

@my_decorators
def greet():
    name = 'Pradeep'
    print(f'Hellow! {name}')
greet()



def my_decorators1(func):
    def wrapper():
        a = 20
        b = 30
        c = a+b
        print(f"addition---:  {a} + {b} = {c}")
        func()
        a = 9
        b = 8
        c = a * b
        print(f"Multiplication---:  {a} * {b} = {c}")
    return wrapper
@my_decorators1
def greet_func():
    a = 12
    b = 7
    c = a - b
    print(f"Subtraction---:  {a} - {b} = {c}")
# greet_func()
# new_func = my_decorators1(greet_func)
# new_func()"""



def sum_decorator(func):
    def wrapper(*args):
        print('ss')
        result = sum(func(*args))  # Call the original function
        return result    # Sum the returned iterable

    return wrapper

@sum_decorator
def main(*args):
    print('ff')
    return args  # Return the tuple of arguments

print(main(2, 4, 6, 8, 2))




