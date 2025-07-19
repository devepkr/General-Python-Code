import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

"""
Single inheritance
"""

class ParentClass1:
    def func(self):
        print('Parent1 class is called')

class ChildClass1(ParentClass1):
    def func1(self):
        print('Child1 class is called')

single = ChildClass1()
single.func()
single.func1()

"""
Multilevel inheritance in Python is when a class inherits from a parent class, 
and another class inherits from that child class, forming a chain of inheritance
"""
class ParentClass2_1:
    def multilevel_1(self):
        print('Parent class is called')

class ChildClass2_2(ParentClass2_1):
    def multilevel_2(self):
        print('Child class is called')

class GrandChildClass(ChildClass2_2):
    def multilevel_3(self):
        print('Grandchild class is called')

# Example usage
Multilevel = GrandChildClass()
# Multilevel.multilevel_1()
# Multilevel.multilevel_2()
# Multilevel.multilevel_3()

"""
Multiple inheritance in Python occurs when a class inherits from more than one parent class, 
allowing it to access attributes and methods from all parent classes. Here's an example to clarify
"""
print('start multiple Inheritance !!.')
class ParentClass3_1:
    def func1(self):
        print('Parent class 1 is called')

class ParentClass3_2:
    def func2(self):
        print('Parent class 2 is called')

class ChildClass3_4(ParentClass3_1, ParentClass3_2):
    def func3(self):
        print('Child class is called')

# Example usage
multiple = ChildClass3_4()
multiple.func1()
multiple.func2()
multiple.func3()













