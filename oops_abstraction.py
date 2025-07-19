
"""
Abstraction is one of the fundamental principles of Object-Oriented Programming (OOP).
It refers to hiding the internal implementation details and showing only the essential features of an object.
"""
from abc import ABC, abstractmethod


# Abstract base class
class RBI:

    def interest(self):
        pass  # Abstract method (must be implemented by subclasses)


# Child class 1
class SBI(RBI):
    def interest(self):
        return 'SBI interest rate is 10.75'


# Child class 2
class HDFC(RBI):
    def interest(self):
        return 'HDFC interest rate is 11.75'


# Create objects SBI
obj_sbi = SBI()
print(obj_sbi.interest())

# Create objects HDFC
obj_hdfc = HDFC()
print(obj_hdfc.interest())


# Abstract base class
class Vehicle(ABC):

    @abstractmethod
    def move(self):
        pass # Abstract method (must be implemented by subclasses)


class Train(Vehicle):
    def move(self):
        return 'The train is moving on tracks.'


class Helicopter(Vehicle):
    def move(self):
        return 'The helicopter is flying in the air.'


obj_train = Train()
print(obj_train.move())

obj_helicopter = Helicopter()
print(obj_helicopter.move())

