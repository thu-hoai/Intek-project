#!/usr/bin/env python3
import re
import os

def convert_string_to_version_component_numbers(s, *args):
    """
    Convert a string to version component number
    @param:
        -s: string representation of a semantic versioning 3-component number

    @return:
        a tuple composed of 3 integers (major, minor, patch)
    """

    if not isinstance(s, str):
        raise TypeError("Not a string")

    # Standard format of a semantic versioning number
    str_format = "^(\d+\.){0,2}(\d+)$"

    # Data validation
    if not re.match(str_format, s):
        raise TypeError("Not a semantic versioning 3-component number")
    if len(args) != 0:
        raise TypeError("Input only one string")
    if s == "0.0.0" or s == "0.0" or s == "0":
        raise ValueError("Not a version component number")

    # Covert given string to tuple
    semantic_ver = tuple(map(int, s.split('.')))

    # In case of 1-component or 2-component number
    if len(semantic_ver) == 3:
        semantic_ver
    elif len(semantic_ver) == 2:
        semantic_ver += (0,)
    else:
        semantic_ver += (0, 0,)
    return semantic_ver

# Waypoint 2: Compare Versions
def compare_versions(this, other):
    """
    Compare versions
    @param:
        -this: tuple composed of 3 integers (major, minor, patch)
        -other: tuple composed of 3 integers (major, minor, patch)
    @return:
        -1 if 'this' is above 'other'
        -1 if 'this' equals 'other'
        -1 if 'this' is below 'other'
    """

    for tup in (this, other):
        if not isinstance(tup, tuple):
            raise ValueError("Not a tuple")
        if not all([isinstance(x, int) for x in tup]):
            raise ValueError("Not a composed of 3 integers")
        if len(tup) != 3:
            raise ValueError("Not a composed of 3 integers")

    if this > other:
        return 1
    elif this == other:
        return 0
    return -1

# Waypoint 3: Write a Class Version

class Version:
    # Constructor
    def __init__(self, major, minor=0, patch=0):

        # in case of Version has 1 to 3 integers
        if not isinstance(minor, int) or not isinstance(patch, int):
            raise TypeError("Not an integer")
        if isinstance(major, int):
            self.major = major
            self.minor = minor
            self.patch = patch

        # in case of Version accepts a string representation
        # of a semantic versioning 3-component number
        if isinstance(major, str):
            if minor or patch:
                raise ValueError("Only input one string")
            self.major, self.minor, self.patch = \
            convert_string_to_version_component_numbers(major)

        # in case of Version is a tupple from 1 to 3 integers
        if isinstance(major, tuple):
            if minor or patch:
                raise ValueError("Only input a tuple")
            if not all([isinstance(x, int) for x in major]):
                raise ValueError("Not a tuple composed of 3 integers")
            if len(major) > 3:
                raise ValueError("Not a tuple composed of 3 integers")
            self.major = major[0]
            self.minor = major[1] if len(major) > 1 else minor
            self.patch = major[2] if len(major) > 2 else patch

    # Waypoint 6: Compare Version Instances
    def __lt__(self, other):
        if not isinstance(other, Version): # Check class membership of Version
            return NotImplemented
        return ((self.major, self.minor, self.patch) \
                < (other.major, other.minor, other.patch))

    def __le__(self, other):
        if not isinstance(other, Version): # Check class membership of Version
            return NotImplemented
        return ((self.major, self.minor, self.patch) \
                <= (other.major, other.minor, other.patch))

    def __gt__(self, other):
        if not isinstance(other, Version): # Check class membership of Version
            return NotImplemented
        return ((self.major, self.minor, self.patch) \
                > (other.major, other.minor, other.patch))

    def __ge__(self, other):
        if not isinstance(other, Version): # Check class membership of Version
            return NotImplemented
        return ((self.major, self.minor, self.patch) \
                >= (other.major, other.minor, other.patch))

    def __eq__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return (
            self.major == other.major
            and self.minor == other.minor
            and self.patch == other.patch)

    def __ne__(self, other):
        if not isinstance(other, Version): # Check class membership of Version
            return NotImplemented
        return ((self.major, self.minor, self.patch) \
                != (other.major, other.minor, other.patch))

    def increment_ver(self):
        """
        Increments the patch number of a semantic versioning 3-component number to 1
        """
        self.patch += 1
        return self.major, self.minor, self.patch

    # Waypoint 4: Compute "Official" String Representations
    def __repr__(self):
        return 'Version({}, {}, {})'.format(self.major, self.minor, self.patch)

    # Waypoint 5: Compute "Informal" String Representation
    def __str__(self):
        st = "{}.{}.{}".format(self.major, self.minor, self.patch)
        return st

# Waypoint 7: Git hooks
if __name__ == '__main__':
    path_name = os.path.abspath("./VERSION")
    # if VERSION exists, Increment patch of Version
    if os.path.exists(path_name):
        if os.path.isfile(path_name):
            with open(path_name, 'r+') as f:
                cur_ver = f.read() # store current version as cur_ver
                # write an update version
                f.seek(0)
                update_infor = Version(cur_ver)
                update_infor.increment_ver()
                f.write(update_infor.__str__())

    # create VERSION file if it does not exist
    else:
        with open(path_name, 'w') as f:
            f.write('1.0.1')

