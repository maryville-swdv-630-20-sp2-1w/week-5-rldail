# Week 5 submission
# Week5.py
# Contains initial timekeeping app objects
# Written by piecing together examples from https://www.dropbox.com/sh/f3vrwom1k7p8kb2/AAC9-qZDh_oac1z4xki94hW-a?dl=0

#!/usr/bin/python3

from __future__ import annotations
import pymysql
import copy
from abc import ABC, abstractmethod

# Singleton
"""
    Combination of examples from the Week 5 Module and
    https://gist.github.com/pazdera/1098129
"""
class SingletonType(type):
    __instance = None

    def __new__(cls, *args, **kw):
        if not cls.__instance:
             cls.__instance = super(SingletonType, cls).__new__(*args, **kw)
        return cls.__instance


class DBConnector(object):
    __metaclass__ = SingletonType

    def __init__(self):
        self.host = 'localhost'
        self.user='sa'
        self.db='HumanResources'    

    def __str__(self):
        return 'Host: {host} User: {user} Database: {db}'.format(host=self.host, user=self.user, db=self.db)

    # Create a new connection
    def create_connection(self):
        # Open the database connection
        connection = pymysql.connect(host=host,
                             user=user,
                             password='secret',
                             db=db,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

        # Create a cursor object
        cursor = connection.cursor()

        # Execute a SQL query
        cursor.execute("SELECT VERSION()")

        # Fetch a single row
        data = cursor.fetchone()
        print ("Database version : %s " % data)

        # Disconnect from the server
        connection.close()


# Prototype
"""
    Mainly templated from https://maryville.instructure.com/courses/43363/pages/prototype?module_item_id=2745137
"""
class Prototype(object):
    def clone(self):
        return copy.deepcopy(self)

class Employee(Prototype):
    def __init__(self, name, loginID, department):
        self.name = name
        self.loginID = loginID
        self.department = department

    def __str__(self):
        return 'Name: {name} Login ID: {loginID} Department: {department}'.format(name=self.name, loginID=self.loginID, department=self.department)


# State
"""
    Examples from https://refactoring.guru/design-patterns/state/python/example
    modified as needed for this exercise
"""
class Context(ABC):
    """
    The Context defines the interface of interest to clients. It also maintains
    a reference to an instance of a State subclass, which represents the current
    state of the Context.
    """

    _state = None
    """
    A reference to the current state of the Context.
    """

    def __init__(self, state:State) -> None:
        self.transition_to(state)

    def transition_to(self, state: State):
        """
        The Context allows changing the State object at runtime.
        """

        print(f"Context: Transition to {type(state).__name__}")
        self._state = state
        self._state.context = self

    """
    The Context delegates part of its behavior to the current State object.
    """

    def request1(self):
        self._state.handle1()

    def request2(self):
        self._state.handle2()


class State(ABC):
    """
    The base State class declares methods that all Concrete State should
    implement and also provides a backreference to the Context object,
    associated with the State. This backreference can be used by States to
    transition the Context to another State.
    """

    @property
    def context(self) -> Context:
        return self._context

    @context.setter
    def context(self, context: Context) -> None:
        self._context = context

    @abstractmethod
    def handle1(self) -> None:
        pass

    @abstractmethod
    def handle2(self) -> None:
        pass


"""
Concrete States implement various behaviors, associated with a state of the
Context.
"""


class ConcreteStateA(State):
    def handle1(self) -> None:
        print("ConcreteStateA handles request1.")
        print("ConcreteStateA wants to change the state of the context.")
        self.context.transition_to(ConcreteStateB())

    def handle2(self) -> None:
        print("ConcreteStateA handles request2.")


class ConcreteStateB(State):
    def handle1(self) -> None:
        print("ConcreteStateB handles request1.")

    def handle2(self) -> None:
        print("ConcreteStateB handles request2.")
        print("ConcreteStateB wants to change the state of the context.")
        self.context.transition_to(ConcreteStateA())





def main():
    # Create the db connection (sort of - at least test that the object is instantiated)
    connector = DBConnector()
    print(connector)
#    connector.create_connection() # commented for test use


    # Create the Eployee prototype object (assuming an IT person, but that can be changed in the clone)
    employee1 = Employee("", "", "IT")

    # Create a couple of clones to verify functionality
    employee2 = employee1.clone()
    employee2.name = "Randy"
    employee2.loginID = "rld123"
    print(employee2)
    
    employee3 = employee1.clone()
    employee3.name = "Terry"
    employee3.loginID = "tlb123"
    print(employee3)


    # Create the state object and run a couple of requests
    context = Context(ConcreteStateA())
    context.request1()
    context.request2()


main()
