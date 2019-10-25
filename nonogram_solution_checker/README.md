
# Nonogram Solution Checker

- This code for whoever need to check if the proposed solution matches the nonogram's solution
---

## Description

- Parameters: specifications and solution as below examples:
    ```python
    specifications = (
    ((2,), (4,), (4,)),
    ((1,), (3,), (3,), (2,), (1,))
    )
    ```

      ```python  
      solution = (
      (0, 1, 0),
      (1, 1, 1),
      (1, 1, 1),
      (0, 1, 1),
      (0, 0, 1)
      )
      ```
- Return: `True` if the suggested solution successfully matches the nonogram's specifications, `False` otherwise.
---
## Installation and Running the tests

- Python3 installation is required to get started (check by using python3 --version)
- Clone this repo to your local machine using `https://github.com/intek-training-jsc/intek-mission-password_format-hoaithu1.git`
- Import file check_nonogram.py and test at below instruction

```python
>>> specifications1 = (
... ((2,), (4,), (4,), (4,), (2,)),
... ((1, 1), (5,), (5,), (3,), (1,))
... )
>>> solution1_true = (
... (0, 1, 0, 1, 0),
... (1, 1, 1, 1, 1),
... (1, 1, 1, 1, 1),
... (0, 1, 1, 1, 0),
... (0, 0, 1, 0, 0)
... )
>>> solution1_false = (
... (0, 1, 0, 0, 0),
... (1, 1, 1, 1, 1),
... (1, 1, 1, 1, 1),
... (0, 1, 1, 1, 0),
... (0, 0, 1, 0, 0)
... )
>>> is_nonogram_resolved(specifications1, solution1_true)
True
>>> is_nonogram_resolved(specifications1, solution1_false)
False
  ```

## Support

Reach out to me (author)at the following place!

- Email at hoai.le@f4.intek.edu.vn
---
