#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from model.map import Map


# Test for wp09
def test_map_object():
    # Perfect case
    # Check data
    assert isinstance(Map.load_map('./map/level1.map').data, list)
    assert isinstance(Map.load_map('./map/level1.map'), Map)


# Test for wp10
def test_map_grip():
    assert Map.load_map('./map/level0.map').height == 32
    assert Map.load_map('./map/level0.map').width == 28
    assert Map.load_map('./map/level0.map').grip[0] == \
        [' ', ' ', ' ', ' ', ' ', ' ', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', ' ', ' ', ' ', ' ', ' ', ' ']


# Test for building graph from map grid
@pytest.mark.parametrize(
    "file_path,x,y,num_of_cells,num_of_intersections",
    [
        ("./map/level0.map", 0, 7, 270, 26),
        ("./map/level1.map", 1, 1, 296, 34)
    ]
)
def test_build_graph(file_path, x, y, num_of_cells, num_of_intersections):
    """Test method buid_graph of class Map"""
    map_level_1 = Map.load_map(file_path)
    cells = map_level_1.build_graph(x, y)

    assert len(cells) == num_of_cells
    assert sum(cell.is_intersection() for cell in cells) == num_of_intersections
    for cell in cells:
        assert len(cell.neighbor_cells) >= 2