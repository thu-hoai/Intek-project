#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from model.level import Level
from model.objects import Pacman
from model.map import Map

# -------------------------------------------------------------
# Test for wp011
@pytest.fixture
def level_object():
    return Level.load(1)

def test_level(level_object):
    assert isinstance(level_object, Level)
    assert level_object.number == 1
    assert isinstance(level_object.pmap, Map)
    assert isinstance(level_object.pacman, Pacman)
    assert isinstance(level_object.ghosts, list)
    assert isinstance(level_object.bonuses, list)

    with pytest.raises(Exception) as excinfo:
        Level(1, None, None)
        assert "the class Level MUST be instantiated using its factory method"\
            in str(excinfo.value)