import time
import math

start_time = time.time()
def is_prime(n):
    """
    Check if given number is a prime or not

    Parameter:
    ------------
    n: integer

    Return:
    ----------
    True
        if n is a prime number
    False
        otherwise
    """
    # Raise errors:
    if n is None:
        return None
    if not isinstance(n, int):
        raise AssertionError("Not a natural number")
    if n < 0:
        raise Error("Not a natural number")

    # Check corner cases
    if n < 2:
        return False
    # Using trial division to test
    n1 = int(math.sqrt(n) + 1)
    for i in range(2, n1):
        if n % i == 0:
            return False
    return True

if __name__ == '__main__':

    # Calculate time execution
    for n in range(1, 100000):
        is_prime(n)
    end_time = time.time()
    print("Time required: ", end_time - start_time)
