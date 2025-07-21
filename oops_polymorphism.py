

"""Method Overloading means defining multiple methods with the same name but different parameters."""

""" METHOD OVERLOADING RUN TIME POLYMORPHISM """
class DemoClass:
    def show(self):
        return 'First version with no arguments'

    def show(self, a):
        return 'Second version with 1 arguments'

    def show(self, a, b):
        return 'Third version with 2 arguments'


obj_demo = DemoClass()
# print(obj_demo.show(3, 6))


""" Method Overriding means defining multiple methods with the different class but same function """


""" METHOD OVERRIDING COMPILE TIME POLYMORPHISM """
class Employee: # parent class
    def work(self):
        print("Employee works 9 to 5")

class Developer(Employee): # child class
    def work(self):
        print("Developer writes code")
        super().work()

class Manager(Developer): # child class
    def work(self):
        print("Manager plans and oversees work")
        super().work()

obj_emp = Manager()
obj_emp.work()

