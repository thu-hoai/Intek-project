#!/usr/bin/env python3
import pytest

from pacman.utils import load_map, simplify_map, compress_map_with_rle,\
    compress_single_string_with_rle, save_map, uncompress_map_with_rle,\
    uncompress_single_string_with_rle
from pacman.constants import GHOST, COLOR_RGB_PACMAN, COLOR_RGB_BLINKY,\
    COLOR_RGB_PINKY, COLOR_RGB_INKY, COLOR_RGB_CLYDE


# Test for wp1
def test_load_map():
    file_path = "./map/level1.amap"
    assert isinstance(load_map(file_path), list)

    error_file_path = "./map/level1.amappp"
    with pytest.raises(FileNotFoundError):
        load_map(error_file_path)

    int_file_path = 123
    with pytest.raises(TypeError):
        load_map(int_file_path)

# Test for wp2
def test_simplify_map():

    error_pac_man_map = '╔════════════╗╔════════════╗'
    with pytest.raises(ValueError):
        simplify_map(error_pac_man_map)

    pac_man_map = [

        '╔════════════╗╔════════════╗',
        '║············║║············║',
        '║·╔══╗·╔═══╗·║║·╔═══╗·╔══╗·║',
        '║·║  ║·║   ║·║║·║   ║·║  ║·║',
        '║·╚══╝·╚═══╝·╚╝·╚═══╝·╚══╝·║',
        '║··························║',
        '║·╔══╗·╔╗·╔══════╗·╔╗·╔══╗·║',
        '║·╚══╝·║║·╚══╗╔══╝·║║·╚══╝·║',
        '║······║║····║║····║║······║',
        '╚════╗·║╚══╗ ║║ ╔══╝║·╔════╝',
        '     ║·║╔══╝ ╚╝ ╚══╗║·║',
        '     ║·║║          ║║·║',
        '     ║·║║ ╔══--══╗ ║║·║',
        '═════╝·╚╝ ║XXXXXX║ ╚╝·╚═════',
        '      ·   ║XXXXXX║   ·',
        '═════╗·╔╗ ╚══════╝ ╔╗·╔═════',
        '     ║·║║          ║║·║',
        '     ║·║║ ╔══════╗ ║║·║',
        '╔════╝·╚╝ ╚══╗╔══╝ ╚╝·╚════╗',
        '║············║║············║',
        '║·╔══╗·╔═══╗·║║·╔═══╗·╔══╗·║',
        '║·╚═╗║·╚═══╝·╚╝·╚═══╝·║╔═╝·║',
        '║···║║················║║···║',
        '╚═╗·║║·╔╗·╔══════╗·╔╗·║║·╔═╝',
        '╔═╝·╚╝·║║·╚══╗╔══╝·║║·╚╝·╚═╗',
        '║······║║····║║····║║······║',
        '║·╔════╝╚══╗·║║·╔══╝╚════╗·║',
        '║·╚════════╝·╚╝·╚════════╝·║',
        '║··························║',
        '╚══════════════════════════╝'
    ]
    assert isinstance(simplify_map(pac_man_map), list)

# -----------------------------------------------------------

# Test for wp4
def test_compress_single_string_with_rle():

    # Provided string is not an interger
    integer = 123
    with pytest.raises(TypeError):
        compress_single_string_with_rle(integer)

    # In case existing characters which is
    # not in the simplified Pac-Man map.
    # This case is "═"
    incorect_string = '*.........══.**............*'
    with pytest.raises(ValueError):
        compress_single_string_with_rle(incorect_string)

    # Best cases
    string = '*............**............*'
    assert isinstance(compress_single_string_with_rle(string), str)
    assert compress_single_string_with_rle(string) == '1*12.2*12.1*'


@pytest.fixture
def simplified_pacman_map():
    return load_map("./map/level1.map")


def test_compress_map_with_rle(simplified_pacman_map):
    # In case the argument is not a list
    str_map = 'abc'
    with pytest.raises(ValueError):
        compress_map_with_rle(str_map)

    # Perfect case
    assert isinstance(compress_map_with_rle(simplified_pacman_map), list)


# -----------------------------------------------------------
# Test for wp5
def test_save_map(simplified_pacman_map):
    wrong_path1 = 123
    with pytest.raises(TypeError):
        save_map(simplified_pacman_map, wrong_path1)
    wrong_path2 = './mappp/level1.rle'
    with pytest.raises(TypeError):
        save_map(simplified_pacman_map, wrong_path2)

# -----------------------------------------------------------
# Test for wp06
@pytest.fixture
def compressed_pacman_map():
    return load_map("./map/level1.rle")


def test_uncompress_single_string_with_rle():

    # Provided string is not an interger
    integer = 123
    with pytest.raises(TypeError):
        uncompress_single_string_with_rle(integer)

    # Best cases
    string = '1*12.2*12.1*'
    assert isinstance(uncompress_single_string_with_rle(string), str)
    assert uncompress_single_string_with_rle(string) == \
        '*............**............*'


def test_uncompress_map_with_rle(compressed_pacman_map):
    # In case the argument is not a list
    str_map = 'abc'
    with pytest.raises(ValueError):
        uncompress_map_with_rle(str_map)

    # Perfect case
    assert isinstance(uncompress_map_with_rle(compressed_pacman_map), list)


