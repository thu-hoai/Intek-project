
# Prime Numbers

- This function for whoever need to check if a number is a prime.
- Parameter: an integer
- Return: True if it is a prime number; False otherwise
- _Note: for those who would like to check execution time, run file is_prime.py._
---

## Installation and Running tests

- Python3 installation is required to get started (check by using python3 --version)
- Clone this repo to your local machine using ` https://github.com/intek-training-jsc/intek-mission-prime_numbers-hoaithu1.git`
- Import file is_prime and test at below instruction

```python
>>> n1 = 12
>>> is_prime(n1)
False
```

```python
>>> n2 = "test"
>>> is_prime(n2)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/ltthoai/Documents/hoaile/datastructure_intek/intek-mission-prime_numbers-hoaithu1/is_prime.py", line 24, in is_prime
    raise AssertionError("Not a natural number")
AssertionError: Not a natural number
```

Note: for those who would like to compute the execution time, follow as below instruction:

```python
>>> import time
>>> start_time = time.time()
>>> for n in range(1, 100000):
...     is_prime(n)
>>> end_time = time.time()
>>> print("Time required: ", end_time - start_time)
0.14101099967956543

```
## Support

Reach out to me (author)at the following place!

- Email at hoai.le@f4.intek.edu.vn
---
