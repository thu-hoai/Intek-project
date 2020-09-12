#!/usr/bin/env python3
import pytest

from model.objects import (Object, Ghost, Blinky, Inky, Clyde, Pinky,
    AnimatedCharacter, Bonus, Pacman)
from pacman.constants import (GHOST, PACMAN, COLOR_RGB_PACMAN, COLOR_RGB_BLINKY,\
    COLOR_RGB_PINKY, COLOR_RGB_INKY, COLOR_RGB_CLYDE, AVAILABLE_BONUS_POINTS)
from model.scene import Scene

# -------------------------------------------------------------
# Test for wp07
def _init_object_best_case():
    x = 12
    y = 22
    symbol = 'ᗧ'
    color = (255, 255, 0)
    return Object(x, y, symbol, color)

@pytest.mark.parametrize('classinfo, expected', [
    (_init_object_best_case(), Object(12, 22, 'ᗧ', (255, 255, 0)))
])

def test_init_object_best_case(classinfo, expected):
    assert classinfo == expected

def test_init_object():
    with pytest.raises(ValueError) as excinfo:
        Object(1.2, 22, 'ᗧ', (255, 255, 0))
        assert "The x-coordinater or x-coordinater must be an integer"\
            in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        Object(12, 22, 12, (255, 255, 0))
        assert "Symbol must be a string" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        Object(12, 22, 'ᗧ', 1)
        assert "The color must be a tupple of 3-component integer and must be in range 0-255"\
            in str(excinfo.value)


# -------------------------------------------------------------
# Test for wp08
def _init_ghost_best_case():
    x = 12
    y = 22
    color = (255, 0, 0)
    return Ghost(x, y, color)

@pytest.mark.parametrize('classinfo, expected', [
    (_init_ghost_best_case(), Ghost(12, 22, (255, 0, 0)))])
def test_init_ghost_best_case(classinfo, expected):
    assert classinfo == expected


def test_object():

    AnimatedCharacter(11, 12, GHOST, COLOR_RGB_PINKY)

    bonus = Bonus(11, 12, u"\U0001F352", AVAILABLE_BONUS_POINTS[u"\U0001F352"])
    assert bonus.symbol ==  "🍒"
    assert bonus.points == AVAILABLE_BONUS_POINTS[u"\U0001F352"]
    with pytest.raises(ValueError) as excinfo:
        Bonus(11, 12, u"\U0001F352", 200)
        assert "Points must be appropriate to the symbol" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        Bonus(11, 12, u"\U0001F352", 10.3)
        assert "Points must be an integer" in str(excinfo.value)

    ghost = Ghost(11, 12, COLOR_RGB_PINKY)
    assert ghost.symbol == GHOST

    pacman = Pacman(11, 12)
    assert pacman.symbol == PACMAN
    assert pacman.color == COLOR_RGB_PACMAN

    blinky = Blinky(12, 22)
    assert blinky.symbol == GHOST
    assert blinky.color == COLOR_RGB_BLINKY

    pinky = Pinky(12, 22)
    assert pinky.symbol == GHOST
    assert pinky.color == COLOR_RGB_PINKY

    inky = Inky(12, 22)
    assert inky.symbol == GHOST
    assert inky.color == COLOR_RGB_INKY

    clyde = Clyde(12, 22)
    assert clyde.symbol == GHOST
    assert clyde.color == COLOR_RGB_CLYDE

import curses
# -------------------------------------------------------------
# Test for wp15

def test_animated_characters():
    char = AnimatedCharacter(11, 12, PACMAN, COLOR_RGB_PACMAN)
    char.set_direction(1, -1)
