# Password Format

Write a function `check_password` that accepts an argument `password` (a string) and that returns `True` if this password complies with a mandatory format, `False` otherwise.

A password MUST contain at least `1` uppercase letter, at least one (1) lowercase letter, at least `1` numeric digit, at least `1` non-word character, but no whitespace, and MUST contain minimum of `8` characters and MUST not exceed more than `35` characters.

For instance:

```python
>>> check_password('abc12345')
False
>>> check_password('abcABC123')
False
>>> check_password('abAB123!')
True
>>> check_password('abAB12!')
False
>>> check_password('abcdefghijkilmnopqrstuvwxyzABCDEFG1!')
False
```

_Note: you **MUST** use the Python standard module [re](https://docs.python.org/3/library/re.html) that provides [**regular expression**](https://www.youtube.com/watch?v=e0xL9o5VibU) matching [operations](https://regex101.com/) similar to those found in Perl._
