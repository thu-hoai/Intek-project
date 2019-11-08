# Products of other Numbers

You have a list of integers, and for each index you want to find the product of every integer except the integer at that index.

Write a function `get_products_of_other_numbers` that takes a list of integers and returns a list of the products.

For example:

```python
>>> get_products_of_other_numbers([1, 7, 3, 4])
[84, 12, 28, 21]
```

by calculating:

```python
  [7 * 3 * 4,  1 * 3 * 4,  1 * 7 * 4,  1 * 7 * 3]
```

Here's the catch: You **CANNOT** use division in your solution!
