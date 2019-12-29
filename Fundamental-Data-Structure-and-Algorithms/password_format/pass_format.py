import re

def check_password(password):

    """
    Check if given password complies with a madatory format.

    Madatory format password: contain at least 1 uppercase letter,
    at least one (1) lowercase letter, at least 1 numeric digit,
    at least 1 non-word char, but no whitespace,
    contain minimum of 8 chars and MUST not exceed more than 35 chars.

    Parameter:
    -----------------
    password: str type

    Returns:
    ------------------
    True or False
        True if this password complies with a mandatory format
        False otherwise.
    """
    # Raise exception
    if password is None:
        return None

    if not isinstance(password, str):
        raise TypeError('Your password is not a string')

    # List of all conditions required
    list_condition = ["[A-Z]", "[0-9]", "[\W]", "^.{8,35}$", "[a-z]"]
    # Check if given password complies with required format
    if re.findall("[\s]", password) != []:
        return False
    for char in list_condition:
        if re.findall(char, password) == []:
            return False
    return True

if __name__ == '__main__':
    pass1 = "abc12345"
    try:
        print(check_password(pass1))
    except:
        pass

    pass2 = "abcABC123"
    try:
        print(check_password(pass2))
    except:
        pass

    pass3 = "abAB123!"
    try:
        print(check_password(pass3))
    except:
        pass

    pass4 = "abcdefghijkilmnopqrstuvwxyzABCDEFG1!"
    try:
        print(check_password(pass4))
    except:
        pass

    pass5 = "abAB123! abAB123!"
    try:
        print(check_password(pass5))
    except:
        pass

    pass6 = 12345
    try:
        print(check_password(pass6))
    except:
        pass
