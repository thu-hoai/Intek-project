# Prime Numbers

A [prime number](https://en.wikipedia.org/wiki/Prime_number) is a natural number that has exactly two distinct positive divisors. A prime number cannot be formed by multiplying two smaller natural numbers. To put it another way, a prime number is a natural number whose only factors are 1 and itself.

_Note: 1 is not a prime number because 1 only has one positive divisor (itself)._

![Prime Numbers](prime_numbers.png)

The first few prime numbers are 2, 3, 5, 7, 11, 13, 17, 19, 23 and 29.

For example, 3 is a prime because the only ways of writing it as a product, 1 × 3 or 3 × 1, involve 3 itself. However, 6 is not a prime number because it is the product of two numbers (2 × 3) that are both smaller than 6.

Write a function `is_prime` that take an argument `n` representing a natural number and returns `True` if this natural number is a prime number, `False` otherwise.

For example:

```python
>>> is_prime(0)
False
>>> is_prime(1)
False
>>> is_prime(2)
True
>>> is_prime(0)
Traceback (most recent call last):
  File "<input>", line 1, in <module>
  File "<input>", line 32, in is_prime
AssertionError: Not a natural number
>>> is_prime('Hello!')
Traceback (most recent call last):
  File "<input>", line 1, in <module>
  File "<input>", line 32, in is_prime
AssertionError: Not a natural number
```

Let's test our function on the first 20 natural numbers:

```python
>>> for n in range(1, 21):
...     print(n, is_prime(n))
1 False
2 True
3 True
4 False
5 True
6 False
7 True
8 False
9 False
10 False
11 True
12 False
13 True
14 False
15 False
16 False
17 True
18 False
19 True
20 False
```

This function works. It correctly identifies the prime numbers.

Your function may also work. But how fast is your function? Let's find out by doing a larger test. Compute the time it is required to test the integers up to 100,000.

```python
>>> import time
>>> start_time = time.time()
>>> for n in range(1, 100000):
...     is_prime(n)
>>> end_time = time.time()
>>> print("Time required: ", end_time - start_time)
0.14101099967956543
```

If your function takes more that 1 second to execute, well... there is room for improvement! :)
