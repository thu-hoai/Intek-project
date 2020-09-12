#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build all constants of Pac Man Game"""

# ==============================
# Game controls

READY_STATE = "READY"
class Directions:
    UP = 'up'
    RIGHT = 'right'
    DOWN = 'down'
    LEFT = 'left'


class GameControls:
    # Set Game speed
    FRAME_PER_SECOND = 7
    MS_PER_FRAME = 1000 // FRAME_PER_SECOND
    READY_STATE_DURATION = 3
    PACMAN_DEAD_DURATION = 4
    GHOSTS_SCARED_DURATION = 10
    GHOST_EYES_DURATION = 10
    GHOSTS_FLASH_WHITE = 2
    GHOSTS_BLUE_DURATION = GHOSTS_SCARED_DURATION - GHOSTS_FLASH_WHITE
    BLINKY_CHASE_PACMAN = 8
    # Symbols Changes
    SKULL = "💀"
    COLLISION = "💥"
    LIVES = 4
    EYES = "👀"
    # Decide quit keys
    QUIT_KEY = ord('q')
    # Initial score each level
    INITIAL_SCORE = 0
    EATEN_GHOST_POINTS = {
        1: 200,
        2: 400,
        3: 800,
        4: 1600
    }

# =========================================
# Symbol for characters
PACMAN = u'\u15e7'  # "ᗧ"
GHOST = u'\u15e3'  # "ᗣ"
INITIAL_LEVEL = 0  # Default level number

# =========================================
# Symbol for drawing map
WALL = "*"
GO = "-"
POINTS = "."
ENERGIZER = "o"
LEFT_TOP = u'\u2554'         # ╔
VERTICAL = u'\u2551'         # ║
LEFT_BOTTOM = u'\u255a'      # ╚
RIGHT_TOP = u'\u2557'        # ╗
RIGHT_BOTTOM = u'\u255d'     # ╝
HORIZONTAL = u'\u2550'       # ═
ROCK = "x"

# =========================================

# Available colors
COLOR_RGB_PACMAN = COLOR_RGB_READY_STATE = (255, 255, 0)
COLOR_RGB_BLINKY = (255, 0, 0)
COLOR_RGB_PINKY = (255, 184, 255)
COLOR_RGB_INKY = (0, 255, 255)
COLOR_RGB_CLYDE = (255, 184, 82)
COLOR_RGB_WALL = (33, 33, 255)
COLOR_RGB_POINTS = (250, 184, 150)
COLOR_RGB_WHITE = (255, 255, 255)

# =========================================
# Position
DRAWING_CHARACTERS = {
    "*": [
        u"\u2550",  # 0 "═"]
        u"\u2551",  # 1 "║"
        u"\u2554",  # 2 "╔"
        u"\u2557",  # 3 "╗"
        u"\u255A",  # 4 "╚"
        u"\u255D",  # 5 "╝"
    ],
    ".": u"\u00B7",  # "·"
    "o": u"\u2022"  # "•"
}

# =========================================
# Validate data for Pacman game
GHOSTS_LIST = ['blinky', 'pinky', 'inky', 'clyde']
AVAILABLE_BONUSES_LIST = [
    'cherry', 'strawberry', 'orange', 'apple', 'melon',
    'bell', 'key']
AVAILABLE_SYMBOL_IN_MAP = ["*", ".", ' ', 'o', 'x', '-']
AVAILABLE_BONUS_POINTS = {
    "🍒": 100,  # u"\U0001F352",
    "🍓": 300,  # u"\U0001F353",
    "🍊": 500,
    "🍎": 700,
    "🍈": 1000,
    "🔔": 3000,
    "🔑": 5000
}


# =========================================
# Define color number for characters
DEFAULT_BACKGROUND_COLOR = (0, 0, 0)
COLOR_NUMBER_DICT = {
    COLOR_RGB_PACMAN: 8,
    COLOR_RGB_BLINKY: 9,
    COLOR_RGB_PINKY: 10,
    COLOR_RGB_INKY: 11,
    COLOR_RGB_CLYDE: 12,
    COLOR_RGB_WALL: 13,
    COLOR_RGB_POINTS: 14,
    COLOR_RGB_WHITE: 15,
    DEFAULT_BACKGROUND_COLOR: 16,
    COLOR_RGB_READY_STATE: 17

}


