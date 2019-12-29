---
title: Left Rotation
level: beginner
language: eng
topics: [python, array]
waypoints: 1
---

# Left Rotation

A left rotation operation on an array of size `n` shifts each of the array's elements `1` unit to the left. For example, if `2` left rotations are performed on array `[1, 2, 3, 4, 5]`, then the array would become `[3, 4, 5, 1, 2]`:

```text
[1, 2, 3, 4, 5] -> [2, 3, 4, 5, 1] -> [3, 4, 5, 1, 2]
```

Write a function `left_rotation` that takes an array of integers and a number, and returns an array which elements have been rotated this number of times to the left.

For example:

```python
>>> left_rotation([1, 7, 0, 4, 1, 9, 7, 1], 4)
[1, 9, 7, 1, 1, 7, 0, 4]
```
