import pprint

# WAYPOINT01
def fibonacci_direct_recursive(n):
    """
    Take n as a whole number and returns the corresponding fibonacci number

    Parameter
    --------------
    n
        integer

    Return
    --------------
    the corresponding fibonacci number
        integer
    """
    # Raise error
    if not isinstance(n, int) or n < 0:
        raise ValueError("Not a whole number")
    
    # Base cases
    if n <= 1: 
        return n
    # Recursive cases
    return fibonacci_direct_recursive(n - 1) + fibonacci_direct_recursive(n - 2)

# WAYPOINT02
def fib_tail_recursive(n, a = 0, b = 1):

    # Raise error
    if not isinstance(n, int):
        raise TypeError("Not a whole number")

    if n < 0:
        raise ValueError("Not a whole number")
    
    # Base caseS
    if n == 0:
        return a
    if n == 1:
        return b
    # Recursive cases
    return fib_tail_recursive(n - 1, b, a + b)

def fibonacci_tail_recursive(n):
    """
    Take n as a whole number and returns the corresponding fibonacci number
    Method: use tail rescursion

    Parameter
    --------------
    n
        integer

    Return
    --------------
    the corresponding fibonacci number
        integer
    """
    return fib_tail_recursive(n, 0, 1)

if __name__ == '__main__':

    try:
        print(fibonacci_direct_recursive(-5))
    except:
        pass

    try:
        print(fibonacci_direct_recursive("hello"))
    except:
        pass

    print(fibonacci_direct_recursive(0))
    print(fibonacci_direct_recursive(1))
    print(fibonacci_direct_recursive(2))
    print(fibonacci_direct_recursive(8))
    print([fibonacci_direct_recursive(i) for i in range(20)])
    
    pprint.pprint([fibonacci_tail_recursive(i) for i in range(0, 200, 10)])

