
# Left Rotation

- This code for those who would like to get an array which elements have been rotated as given number of times to the left.
---

## Description

- Parameters: array of integers and a number.
`For example: ([1, 7, 0, 4, 1, 9, 7, 1], 4)`
Every other format will be raised as an error (show more as below running test cases)
- Return: An array which elements have been rotated this number of times to the left.
---

## Installation

- Python3 installation is required to get started (check by using python3 --version)
- Clone this repo to your local machine using `https://github.com/intek-training-jsc/intek-mission-password_format-hoaithu1.git`
- Import left_rotation and test as below instruction:

```python
>>> a1 = ([1, 7, 0, 4, 1, 9, 7, 1], 1)
>>> left_rotation(a1)
[7, 0, 4, 1, 9, 7, 1, 1]
```
A left rotation operation on an array of size n shifts each of the array's elements 4 unit to the left. In this case, it returns `[7, 0, 4, 1, 9, 7, 1, 1]`

```python
>>> a2 = ([1, 7, 0, 4, 1, 9, "7", 1], 1)
>>> left_rotation(a2)
```
It raises a` TypeError: Not an integer`

```python
>>> a3 = ([1, 7, 0, 4, 1, 9, 7, 1], "1")
>>> left_rotation(a3)
```
It raises a` TypeError: Not an integer`

```python
>>> a4 = ([1, 7, 0, 4, 1, 9, 7, 1, 1])
>>> left_rotation(a4)
```
It raises a` TypeError: Not an array of integers and a number`


## Support

Reach out to me (author)at the following place!

- Email at hoai.le@f4.intek.edu.vn
---
