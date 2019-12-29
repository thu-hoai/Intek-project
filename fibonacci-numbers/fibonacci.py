import pprint
from functools import lru_cache
import sys
sys.setrecursionlimit(1500)

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
    if not isinstance(n, int):
        raise TypeError("Not a whole number")
    if n < 0:
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

# WAYPOINT 03
def fibonacci_iterative(n):
    """
    Take n as a whole number and returns the corresponding fibonacci number
    Method: use iteration
    Parameter
    --------------
    n
        integer
    Return
    --------------
    the corresponding fibonacci number
        integer
    """
    var_n1 = 0  # variable for (n - 1)
    var_n2 = 1 # variable for (n - 2)

    if n == 0: # corner case
        return var_n1
    else:
        for i in range(1, n):
            sum_tmp = var_n1 + var_n2
            var_n1, var_n2 = var_n2, sum_tmp
        return var_n2

# WAYPOINT04
@lru_cache(maxsize = 1000) # set cache
def fibonacci_direct_recursive_memoized(n):
    """
    Take n as a whole number and returns the corresponding fibonacci number
    Method: using memoization
    Parameter
    --------------
    n
        integer
    Return
    --------------
    the corresponding fibonacci number
        integer
    """
    # Base cases
    if n <= 1:
        return n
    # Recursive cases
    return fibonacci_direct_recursive_memoized(n - 1) + fibonacci_direct_recursive_memoized(n - 2)
  
# WAYPOINT05
def fibonacci_golden_ratio(max_occurrences_number = 10):
    """
    Count the number of times rations keep the same value and return the ratio
    Parameter
    ------------------
    max occurences number
        integer
        the number of times ratios keep the same value
        over several successive ratio calculations
    Return
    -------------------
        float
        The ratio which keeps the same value 'max_occurrences_number' times
    """
    # Initialize for the number of loops
    i = 1 
    # Initialize to count ratio every the ratios keep the same value
    count_golden_ratio = 0 

    # Run until the number of times ratios keep the same value 
    # is the same as max_occurrences_number
    while True:

        a1 = fibonacci_direct_recursive_memoized(i)
        a2 = fibonacci_direct_recursive_memoized(i + 1)
        a3 = fibonacci_direct_recursive_memoized(i + 2)

        # Calculate golden_ration at two consecutive times
        golden_ratio1 = a2 / a1
        golden_ratio2 = a3 / a2
        i += 1

        if golden_ratio1 == golden_ratio2:
            count_golden_ratio += 1
        else:
            count_golden_ratio = 0

        if count_golden_ratio == max_occurrences_number:
            return golden_ratio1

 
if __name__ == '__main__':   
    
    # Testing for waypoint_01
    print([fibonacci_direct_recursive(i) for i in range(20)])
    
    # Testing for waypoint_02    
    pprint.pprint([fibonacci_tail_recursive(i) for i in range(0, 200, 10)])
    
    # Testing for waypoint_03
    pprint.pprint([fibonacci_iterative(i) for i in range(0, 400, 20)])
   
    # Testing for waypoint_04
    def test_fibonacci_direct_recursive(n):
        from datetime import datetime
        start_time = datetime.now()
        values = [fibonacci_direct_recursive(i) for i in range(n)]
        print(f"Function executed in {(datetime.now() - start_time).total_seconds()} s")
        return values
    test_fibonacci_direct_recursive(34)

    def test_fibonacci_direct_recursive_memoized(n):
        from datetime import datetime
        start_time = datetime.now()
        values = [fibonacci_direct_recursive_memoized(i) for i in range(n)]
        print(f"Function executed in {(datetime.now() - start_time).total_seconds()} s")
        return values
    test_fibonacci_direct_recursive_memoized(34)

    # Testing for waypoint_05
    print(fibonacci_golden_ratio())
    print(fibonacci_golden_ratio(100))
