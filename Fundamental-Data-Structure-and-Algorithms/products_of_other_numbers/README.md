
# Products of other Numbers

## Description

- This function for whoever need to return a list of the products of every integer except the integer at that index.
- Parameter: a list of integers, for ex: `[1, 7, 3, 4]`
- Return: A list of products

## Installation and Running the tests

- Python3 installation is required to get started (check by using python3 --version)
- Clone this repo to your local machine using `https://github.com/intek-training-jsc/intek-mission-products_of_other_numbers-hoaithu1.git`
- Import product_other_num and test at below instruction

```python
>>> from product_other_num import *
>>> get_products_of_other_numbers([1, 7, 3, 4])
[84, 12, 28, 21]

```
It returns `[84, 12, 28, 21]` by calculating `[7 * 3 * 4,  1 * 3 * 4,  1 * 7 * 4,  1 * 7 * 3]`

```python
>>> get_products_of_other_numbers([0, 1, 2, 3, "5"])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/ltthoai/Documents/hoaile/datastructure_intek/intek-mission-products_of_other_numbers-hoaithu1/product_other_num.py", line 21, in get_products_of_other_numbers
    raise TypeError("Not an integer")
TypeError: Not an integer
>>> 
```

## Support

Reach out to me (author)at the following place!

- Email at hoai.le@f4.intek.edu.vn
---
