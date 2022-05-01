"""
RPN Calculator Stack Implementation
Loren Pena
Purpose of this is to create a Reverse Polish Notation (RPN) calculator using NumPy arrays and stack.
"""

import numpy as np

class MyStack:
    # Constants
    MAX_CAPACITY = 100000
    DEFAULT_CAPACITY = 10

    # Initializer method
    def __init__(self, default_item, capacity=DEFAULT_CAPACITY):
        # If the capacity is bad, fail right away
        if not self.validate_capacity(capacity):
            raise ValueError("Capacity " + str(capacity) + " is invalid")
        self.capacity = capacity
        self.default_item = default_item

        # Make room in the stack and make sure it's empty to begin with
        self.clear()

    def clear(self):
        # Allocate storage the storage and initialize top of stack
        self.stack = np.zeros([self.capacity], dtype=int)
        self.top_of_stack = 0

    @classmethod
    def validate_capacity(cls, capacity):
        return 0 <= capacity <= cls.MAX_CAPACITY

    def push(self, item_to_push):
        if self.is_full():
            raise IndexError("Push failed - capacity reached")

        self.stack[self.top_of_stack] = item_to_push
        self.top_of_stack += 1

    def pop(self):
        if self.is_empty():
            raise IndexError("Pop failed - stack is empty")

        self.top_of_stack -= 1
        return self.stack[self.top_of_stack]

    def is_empty(self):
        return self.top_of_stack == 0

    def is_full(self):
        return self.top_of_stack == self.capacity

    def get_capacity(self):
        return self.capacity


class RpnCalculator:
    """
    One object of this class represents a Reverse Polish Notation (RPN) calculator:
    """
    ADDITION = "+"
    SUBTRACTION = "-"
    MULTIPLICATION = "*"
    FLOOR = "//"

    @staticmethod
    def eval(rpn_expression):
        """
        Method takes a string expression of RPN and returns the mathematical result as a int.
        """
        parsed = RpnCalculator.parse(rpn_expression)
        result = RpnCalculator.eval_tokens(parsed)
        return result

    @staticmethod
    def parse(rpn_expression):
        """
        Method takes a string expression of RPN and returns the expression parsed.
        """
        return rpn_expression.split()

    @staticmethod
    def eval_tokens(tokens):
        """
        Method takes a list of tokens and calculates results of the expressions
        integers and mathematical operators in the list.
        Returns outcome of the mathematical expression as int.
        """
        my_stack = MyStack(1, 1000)
        for token in tokens:
            try:
                token_int = int(token)
                my_stack.push(token_int)
            except ValueError:
                right_arg = my_stack.pop()
                left_arg = my_stack.pop()
                if token == RpnCalculator.ADDITION:
                    my_stack.push(left_arg + right_arg)
                elif token == RpnCalculator.SUBTRACTION:
                    my_stack.push(left_arg - right_arg)
                elif token == RpnCalculator.FLOOR:
                    my_stack.push(left_arg // right_arg)
                elif token == RpnCalculator.MULTIPLICATION:
                    my_stack.push(RpnCalculator.mult(left_arg, right_arg))
                else:
                    raise ValueError("Unknown operator")
        if my_stack.top_of_stack // 2 != 0:
            raise IndexError("Not enough operator")
        else:
            return my_stack.pop()

    @staticmethod
    def mult(x, y):
        """
        mult method calculates recursively the product of two integers x and y.
        Returns the product of the integers.
        """
        if y == 0 or x == 0:
            return 0
        if x < 0 and y < 0:
            absolute_x = abs(x)
            absolute_y = abs(x)
            return absolute_y + RpnCalculator.mult(absolute_y, absolute_x - 1)
        elif y < 0 and x > 0:
            return y + RpnCalculator.mult(y, x - 1)
        else:
            return x + RpnCalculator.mult(x, y - 1)

def rpn_calcuator_test():
    """
    Method is for testing or RpnCalculator class.
    """
    rpn = RpnCalculator()

    try:
        rpn1 = RpnCalculator("Hello World")
        print("rpn1 = RpnCalculator('Hello World') This should not work")
    except Exception as e:
        print(str(e))

    try:
        rpn.eval('')
        print("Failed test: expected My_Stack to fail .pop()")
    except Exception as e:
        print("'' fails to be evaluated: " + str(e))

    try:
        rpn.eval("1 1 &")
        print("Failed test: & is a unknown operator and should not be handled.")
    except Exception as e:
        print("'1 1 &' fails to be evaluated: " + str(e))

    try:
        rpn.eval("1 1")
        print("Failed test: not mathematically solvable.")
    except Exception as e:
        print("'1 1' fails to be evaluated: " + str(e))
    try:
        rpn.eval("1 1 + +")
        print("Failed test: not mathematically solvable .pop() should fail. ")
    except Exception as e:
        print("'1 1 + +' fails to be evaluated: " + str(e))

    try:
        rpn.eval("Random Junk")
        print("Failed test: .pop() should fail. ")
    except Exception as e:
        print("'Random Junk' fails to be evaluated: " + str(e))

    print("(1) = {}".format(rpn.eval("1")))
    print("(1 1 +) = {}".format(rpn.eval("1 1 +")))
    print("(15 5 +) = {}".format(rpn.eval("15 5 +")))
    print("(15 -5 *) = {}".format(rpn.eval("15 -5 *")))
    print("(1 1 1 + -) = {}".format(rpn.eval("1 1 1 + -")))
    print("(15 7 1 1 + - // 3 * 2 1 1 + + -) = {}".format(rpn.eval("15 7 1 1 + - // 3 * 2 1 1 + + -")))
    print("\nTesting mult()")
    print("(-5 27 *) = {}".format(rpn.eval("-5 27 *")))
    print("(5 -27 *) = {}".format(rpn.eval("-5 27 *")))
    print("(-5 -27 *) = {}".format(rpn.eval("-5 -27 *")))
    print("(-5 0 *) = {}".format(rpn.eval("-5 0 *")))
    print("(0 5 *) = {}".format(rpn.eval("0 5 *")))
    print("(0 0 *) = {}".format(rpn.eval("0 0 *")))
    try:
        print("(0 kk *) = {}".format(rpn.eval("0 kk *")))
        print("This should not work")
    except Exception as e:
        print("'0 kk *' fails to be evaluated: " + str(e))


if __name__ == "__main__":
    rpn_calcuator_test()
"""OUTPUT OF RUN
RpnCalculator() takes no arguments
'' fails to be evaluated: Pop failed - stack is empty
'1 1 &' fails to be evaluated: Unknown operator
'1 1' fails to be evaluated: Not enough operator
'1 1 + +' fails to be evaluated: Pop failed - stack is empty
'Random Junk' fails to be evaluated: Pop failed - stack is empty
(1) = 1
(1 1 +) = 2
(15 5 +) = 20
(15 -5 *) = -75
(1 1 1 + -) = -1
(15 7 1 1 + - // 3 * 2 1 1 + + -) = 5

Testing mult()
(-5 27 *) = -135
(5 -27 *) = -135
(-5 -27 *) = 25
(-5 0 *) = 0
(0 5 *) = 0
(0 0 *) = 0
'0 kk *' fails to be evaluated: Pop failed - stack is empty
"""
