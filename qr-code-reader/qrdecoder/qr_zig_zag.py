#!/usr/bin/env python3
"""Funcs To Support Get Coordinates"""

def _add_to_tuple(tup1, tup2):
    return ((tup1[0] + tup2[0]), (tup1[1] + tup2[1]))


def _get_next_is_up(current, size):
    is_even_col = True
    result = []
    while current[0] >= 0:
        result.append(current)
        if is_even_col is True:
            step = (0, -1)
        else:
            step = (-1, 1)
        next_ele = _add_to_tuple(current, step)
        current = next_ele

        is_even_col = not is_even_col
        continue
    return result

def _get_next_is_down(current, size):
    is_even_col = True
    result = []
    while (current[0] <= size - 1 and current[1] != size - 1):
        result.append(current)
        if is_even_col is True:
            step = (0, -1)
        else:
            step = (1, 1)
        next_ele = _add_to_tuple(current, step)
        current = next_ele
        is_even_col = not is_even_col
        continue
    return result

# Get data and error correctionc coordinaters
def _get_data_and_error_correction_area_coordinaters(current, size):
    is_up = True
    result = []
    while current[1] >= 0 and current[0] <= size - 1:
        if is_up:
            block = _get_next_is_up(current, size)
        else:
            block = _get_next_is_down(current, size)
        result += block
        is_up = not is_up
        step = (0, -1)
        current = _add_to_tuple(block[-1], step)
        if current[1] == 6:
            step = (0, -2)
            current = _add_to_tuple(block[-1], step)
        continue
    return result
