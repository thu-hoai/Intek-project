#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build Preliminaries of PacMan Game"""

import copy
import os.path
from pacman.constants import (
    DRAWING_CHARACTERS, WALL, POINTS, ENERGIZER, GO, AVAILABLE_SYMBOL_IN_MAP,
    LEFT_TOP, VERTICAL, LEFT_BOTTOM, RIGHT_TOP, RIGHT_BOTTOM, HORIZONTAL)


def load_map(file_pathname):
    """Load Pac-Man Map

    Arguments:
        file_pathname {str} -- the file path name of a Pac-Man map

    Raises:
        FileNotFoundError: Provided file path name is not found
        IOError: Provided file path name can not accessible by read mode

    Returns:
        list -- A list of lines of Pac-Man Map
    """
    if not isinstance(file_pathname, str):
        raise TypeError("Your file path must be a string")
    try:
        # Open the file back and read the contents
        with open(file_pathname, "r") as map_file:
            contents = map_file.read().splitlines()
    # Check if the file or directory at `path` can be found
    except FileNotFoundError:
        raise FileNotFoundError("File does not exist")
    # Check if the file or directory at `path` can be accessed by the program
    except IOError:
        raise IOError("File is not accessible")
    # Returns a list of line
    return contents


def simplify_map(pacman_map):
    """ Simplify Pac-Man Map

    Arguments:
        pacman_map {list} -- a list of line of Pac-Man map

    Raises:
        ValueError: Provided input is not a list

    Returns:
        list -- A simplified version of Pacman-map where:
            the Unicode box drawing characters "═", "║", "╔", "╗", "╚",
                and "╝" are replaced with the ASCII character "*";
            the Unicode character "·" is replaced with the ASCII character
                "." (dot)
    """

    if not isinstance(pacman_map, list):
        raise ValueError("Your input must be a list of lines")

    # Initialize a list to store result
    simplified_map = []

    # Loop in pacman list, then change line by line
    for line in pacman_map:
        for key, values in DRAWING_CHARACTERS.items():
            for value in values:
                if value in line:
                    line = line.replace(value, key)
        simplified_map.append(line)

    return simplified_map


def prettify_map(simplified_map):
    """Convert Simplified to Human-Viewable Pac-Man Map

    Arguments:
        simplified_map {list} -- simplified versions of the Pac-Man maps

    Raises:
        ValueError: Provided map is not a list

    Returns:
        list:  a human-readable version
    """
    if not isinstance(simplified_map, list):
        raise ValueError("Your input must be a list of simplified map")

    # Data processing first
    simplified_map = _process_map_data(simplified_map)
    # Deep copy simplified_map to modify on result_map
    result_map = copy.deepcopy(simplified_map)

    # Store height and with of the map which is proccessed data
    height = len(result_map)
    width = len(result_map[0])

    # Initialize human-readable map
    human_map = []

    for row in range(height):
        for col in range(width):

            # In cases the symbol is NOT WALL: POINTS and ENERGIZER
            if simplified_map[row][col] != WALL:
                if simplified_map[row][col] == POINTS:
                    result_map[row][col] = DRAWING_CHARACTERS[POINTS]
                if simplified_map[row][col] == ENERGIZER:
                    result_map[row][col] = DRAWING_CHARACTERS[ENERGIZER]
                continue

            # In cases symbol is WALL
            # Get 8-neiboughhood-points of the current points
            neighbors_coord_dict = _get_neighbors_symbol(
                row, col, height, width)

            # Change `wall` to Vertical and Horizontal symbol
            _modify_to_vertical_horizontal_symbols(
                row, col, simplified_map, neighbors_coord_dict, result_map)

            # Change `wall` to 4 angle types
            # check and change to ╝ if position is "RIGHT_BOTTOM"
            _modify_to_angle_symbols(
                1, 3, neighbors_coord_dict, simplified_map, result_map, row, col)
            # check and change to ╚ if position is "LEFT_BOTTOM"
            _modify_to_angle_symbols(
                3, 5, neighbors_coord_dict, simplified_map, result_map, row, col)
            # check and change to ╔ if position is "LEFT_TOP
            _modify_to_angle_symbols(
                5, 7, neighbors_coord_dict, simplified_map, result_map, row, col)
            # check and change to ╗ if position is "RIGHT_TOP"
            _modify_to_angle_symbols(
                1, 7, neighbors_coord_dict, simplified_map, result_map, row, col)
            # Handle corner case at 4 border lines
            _modify_to_vertical_corner_case(
                row, col, neighbors_coord_dict, simplified_map, result_map)
    # Concadinate string each of line
    for i, char in enumerate(result_map):
        human_map.append(''.join(char))

    return human_map


def compress_single_string_with_rle(string):
    """Compress a string with rle

    Arguments:
        string {str} -- provided string which is in the simplified Pac-Man map

    Raises:
        TypeError: Provided input is not a string
        ValueError: Existing the character which not in
                    the simplified Pac-Man map

    Returns:
        str -- RLE string
    """
    if not isinstance(string, str):
        raise TypeError("Your input must be a string")

    # Initialize a list to store the character of string
    stack = ["0"]
    # Initialize a count variable represent to the frequency of the character
    count_temp = 0

    for character in string:
        # The given string must be existed in simplified map
        if character not in AVAILABLE_SYMBOL_IN_MAP:
            raise ValueError("Existing the character which not in\
                the simplified Pac-Man map")
        var_temp = character
        count_temp += 1
        if var_temp != stack[-1]:
            stack.append(str(count_temp))
            stack.append(character)
            # Reset for each element
            count_temp = 0
    # Append the counting of the last element
    if var_temp == stack[-1]:
        stack.append(str(count_temp + 1))
    stack = stack[2:]
    # Swap to each pair to get expected result
    for i in range(0, len(stack), 2):
        stack[i+1], stack[i] = stack[i], stack[i+1]
    return ''.join(stack)


def compress_map_with_rle(pacman_map):
    """Compress Pac-Man Map with RLE

    Arguments:
        pacman_map {list} -- a list of line of Pac-Man map

    Raises:
        ValueError: Provided input is not a list

    Returns:
        list -- the compressed version of this map using RLE.
    """
    if not isinstance(pacman_map, list):
        raise ValueError("Your input must be a list of lines")

    # Initialize a list to store all strings
    compressed_map = []
    for line in pacman_map:
        string = compress_single_string_with_rle(line)
        compressed_map.append(string)
    return compressed_map


def save_map(pacman_map, file_pathname):
    """Store the map to file

    Arguments:
        pacman_map {list} -- Pacman map
        file_pathname {str} -- File path name to save

    Raises:
        TypeError: Provided file is not exist
    """
    if not isinstance(file_pathname, str):
        raise TypeError("Your file path must be a string")
    if not os.path.isdir(os.path.dirname(file_pathname)):
        raise TypeError("Provided file's parent directory is not exist")
    if not isinstance(pacman_map, list):
        raise ValueError("Provided pacman map must be a list")
    with open(file_pathname, 'w') as rle_file:
        for line in pacman_map:
            rle_file.write(line)
            rle_file.write('\n')


def uncompress_single_string_with_rle(string):
    """Uncompress a string with rle

    Arguments:
        string {str} -- provided string which is in the compress Pac-Man map

    Raises:
        TypeError: Provided input is not a string

    Returns:
        str -- the uncompressed string
    """
    if not isinstance(string, str):
        raise TypeError("Your input must be a string")

    # Initialize a list to store the character of string
    stack = []

    var_temp = ''
    for character in string:
        if '0' <= character <= '9':
            var_temp += character
        else:
            if var_temp:
                stack.append(character * int(var_temp))
            else:
                stack.append(character)
            # Reset for each character
            var_temp = ''

    return ''.join(stack)


def uncompress_map_with_rle(compressed_map):
    """Uncompress Pac-Man Map RLE verison

    Arguments:
        pacman_map {list} -- a simplified Pac-Man map that was encoded
            with the Run-Length Encoding (RLE) algorithm

    Raises:
        ValueError: Provided input is not a list

    Returns:
        list -- the uncompressed version of this map using RLE.
    """
    if not isinstance(compressed_map, list):
        raise ValueError("Your input must be a list of lines")

    # Initialize a list to store all strings
    uncompressed_map = []
    for line in compressed_map:
        string = uncompress_single_string_with_rle(line)
        uncompressed_map.append(string)
    return uncompressed_map


# Data processing the given map - fill each line by character ` ` to get
# a map with the same line length
def _process_map_data(old_map):
    new_map = []
    width_list = [len(line) for line in old_map]
    max_width = max(width_list)
    for line in old_map:
        if len(line) != max_width:
            sub = (max_width - len(line))*" "
            line += sub
        new_map.append(list(line))
    return new_map


def _modify_to_vertical_horizontal_symbols(
        row, col, simple_map, neighbors_dict, result_map):
    # Change `wall` to Vertical and Horizontal symbol
    point1 = simple_map[neighbors_dict["x1"]][neighbors_dict["y1"]]
    point3 = simple_map[neighbors_dict["x3"]][neighbors_dict["y3"]]
    point5 = simple_map[neighbors_dict["x5"]][neighbors_dict["y5"]]
    point7 = simple_map[neighbors_dict["x7"]][neighbors_dict["y7"]]

    if point1 == WALL and point5 == WALL or point1 == GO or point5 == GO:
        if point3 != WALL or point7 != WALL:
            result_map[row][col] = HORIZONTAL
    if point3 == WALL and point7 == WALL:
        if point1 != WALL or point5 != WALL:
            result_map[row][col] = VERTICAL


def _modify_to_angle_symbols(a, b, dic, simplified_map, result_map, row, col):
    x1 = f"x{a}"
    y1 = f"y{a}"
    x2 = f"x{b}"
    y2 = f"y{b}"

    if a == 5 and b == 7:
        symbol = LEFT_TOP

    if a == 1 and b == 7:
        symbol = RIGHT_TOP

    if a == 3 and b == 5:
        symbol = LEFT_BOTTOM

    if a == 1 and b == 3:
        symbol = RIGHT_BOTTOM

    if simplified_map[dic[x1]][dic[y1]] == WALL \
            and simplified_map[dic[x2]][dic[y2]] == WALL:
        lst = _get_connected_symbols(row, col, dic, a, b, simplified_map)
        if not any([ele == WALL for ele in lst]):
            result_map[row][col] = symbol
        if all([ele == WALL for ele in lst]):
            result_map[row][col] = symbol


def _modify_to_vertical_corner_case(row, col, neigh_dict, old_map, result_map):
    width = len(old_map[0])
    if col == 0:

        if old_map[neigh_dict['x2']][neigh_dict['y2']] == POINTS and \
                old_map[neigh_dict['x3']][neigh_dict['y3']] == POINTS and\
                old_map[neigh_dict['x5']][neigh_dict['y5']] == WALL:
            result_map[row][col] = '═'
        elif old_map[neigh_dict['x7']][neigh_dict['y7']] == POINTS and \
                old_map[neigh_dict['x8']][neigh_dict['y8']] == POINTS and\
                old_map[neigh_dict['x5']][neigh_dict['y5']] == WALL:
            result_map[row][col] = '═'

    elif col == width - 1:
        if old_map[neigh_dict['x3']][neigh_dict['y3']] == POINTS and \
                old_map[neigh_dict['x4']][neigh_dict['y4']] == POINTS and\
                old_map[neigh_dict['x1']][neigh_dict['y1']] == WALL:
            result_map[row][col] = '═'
        elif old_map[neigh_dict['x6']][neigh_dict['y6']] == POINTS and \
                old_map[neigh_dict['x7']][neigh_dict['y7']] == POINTS and\
                old_map[neigh_dict['x1']][neigh_dict['y1']] == WALL:
            result_map[row][col] = '═'


#  Get 8 points surounded the point
# Arguments:
#     row, col {int} -- represent to the current row, col of the provided point
#     height, width {int} -- represent to height and width respectively
#       of the Pacman map

# Returns: (dict) -- [description]
def _get_neighbors_symbol(row, col, height, width):
    #   -------------
    #   | 2 | 3 | 4 |
    #   -------------
    #   | 1 | * | 5 |
    #   -------------
    #   | 8 | 7 | 6 |
    #   -------------
    neighbors_coordinates = [
        0,
        (row, max(col-1, 0)),                               # point 1
        (max(row-1, 0), max(col-1, 0)),                     # point 2
        (max(row-1, 0), col),                               # point 3
        (max(row-1, 0), min(col+1, width - 1)),             # point 4
        (row, min(col+1, width - 1)),                       # point 5
        (min(row+1, height - 1), min(col+1, width - 1)),    # point 6
        (min(row+1, height - 1), col),                      # point 7
        (min(row+1, height - 1), max(col-1, 0))             # point 8
    ]

    neighbors_coord_dict = {}
    for i in range(1, len(neighbors_coordinates)):
        neighbors_coord_dict[f'x{i}'] = neighbors_coordinates[i][0]
        neighbors_coord_dict[f'y{i}'] = neighbors_coordinates[i][1]

    return neighbors_coord_dict


def _get_connected_symbols(row, col, neighbors_dict, a, b, simplified_map):
    # 1 =< a, b <= 8
    #                3
    #   bottom_right ║║ bottom_left
    #             2  ║║  4
    #           ═════╝╚═════
    #        1  ═════╗╔═════  5
    #             8  ║║  6
    #     top_right  ║║  top_left
    #                 7

    height = len(simplified_map)
    width = len(simplified_map[0])
    if a == 1 and b == 3:
        c = 2
    if a == 3 and b == 5:
        c = 4
    if a == 5 and b == 7:
        c = 6
    if a == 1 and b == 7:
        c = 8
    # Get a list that represent the connective points

    lst1 = []
    for i in range(1, 9):
        symbol = simplified_map[neighbors_dict[f'x{i}']
                                ][neighbors_dict[f'y{i}']]
        if col == 0:
            if i not in (a, b, c, 1, 2, 8):
                lst1.append(symbol)

        elif row == 0:
            if i not in (a, b, c, 2, 3, 4):
                lst1.append(symbol)

        elif row == height - 1:
            if i not in (a, b, c, 6, 7, 8):
                lst1.append(symbol)

        elif col == width - 1:
            if i not in (a, b, c, 4, 5, 6):
                lst1.append(symbol)

        else:
            if i not in (a, b, c):
                lst1.append(symbol)

    return lst1
