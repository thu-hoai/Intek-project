#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build Level of Game"""

import os.path
import time
import curses
from model.map import Map
from model.level import Level
from model.color_palette import Palette
from model.objects import Pacman, Bonus, Blinky, Pinky, Inky, Clyde
from pacman.constants import (
    PACMAN, GHOST, POINTS, ENERGIZER, DRAWING_CHARACTERS, COLOR_NUMBER_DICT,
    COLOR_RGB_CLYDE, COLOR_RGB_INKY, COLOR_RGB_PACMAN, COLOR_RGB_BLINKY,
    COLOR_RGB_PINKY, COLOR_RGB_WALL, COLOR_RGB_POINTS, WALL, COLOR_RGB_WHITE,
    COLOR_RGB_READY_STATE, DEFAULT_BACKGROUND_COLOR)
from pacman.constants import GameControls


class Scene:
    """A Class represents to the scene which is the window where
        game engine builds and places game objects."""

    def __init__(self, window, level):
        """The constructor of the Scene Class

        Arguments:
            window {curses.window} -- A `window` pnkect which represents
                the whole screen.

            level {Level} -- A level object which represents
                the Pac-Man level to play.

        Raises:
            ValueError: Provided `level` is not a `Level` object
        """
        if not isinstance(level, Level):
            raise ValueError("Provided level must be a Level object")
        self.window = window
        self.level = level

    def render(self):
        # Register all composite colors
        self.register_color_palette()
        self.window.clear()
        try:
            # Screen1: Scores, Life, Number of Screen Cleared
            self.__draw_screen_1()

            # Screen 2: Map with Dots and Power Capsule
            self.__draw_screen_2()

            # Screen 3: Pac-Man, Ghosts, and Bonus Fruit
            self.__draw_screen_3()

            energizer_list = self.level.pmap.energizer_coordinates
            self.window.addstr(1, 1, str(energizer_list))
        except curses.error:
            pass
        self.window.refresh()

    @staticmethod
    # Get the x-coordinater to align the text at the center of the box
    # Arguments:
    #     box_width {int} -- the width of box
    #     x_left_top {int} -- x-coordinater of the left top
    #     x_right_top {int} -- x-coordinater of the right top
    #     message {str} -- the message that is displayed at the center
    #         of the box
    # Returns:
    #     int -- x-coordinater to align the text at the center of the box
    def _get_center_position(x_left_top, x_right_top, message):

        # Calculate center column, and then adjust starting position based
        # on the length of the message
        half_length_of_message = len(message) // 2

        middle_column = (x_left_top + x_right_top) // 2
        x_position = middle_column - half_length_of_message

        return x_position

    @staticmethod
    # Get the pair number of the color_pair
    def _get_pair_number_of_color(color):
        pair_number = COLOR_NUMBER_DICT[color] - 7
        return curses.color_pair(pair_number)

    @staticmethod
    # Register all the colors using for Pacman Game
    def register_color_palette():
        curses.start_color()
        palette = Palette()
        palette.get_composite_color(COLOR_RGB_PACMAN)
        palette.get_composite_color(COLOR_RGB_BLINKY)
        palette.get_composite_color(COLOR_RGB_PINKY)
        palette.get_composite_color(COLOR_RGB_INKY)
        palette.get_composite_color(COLOR_RGB_CLYDE)
        palette.get_composite_color(COLOR_RGB_WALL)
        palette.get_composite_color(COLOR_RGB_POINTS)
        palette.get_composite_color(COLOR_RGB_WHITE)
        palette.get_composite_color(DEFAULT_BACKGROUND_COLOR)
        palette.get_composite_color(COLOR_RGB_READY_STATE)

    # Draw Screen1: Scores, Life, Number of Screen Cleared

    def __draw_screen_1(self):
        # Calculate to display text
        width = self.level.pmap.width
        height = self.level.pmap.height

        # Get the heights between map to screen
        y_distance, x_distance = self.__calculate_offset()

        # Design box to display "1UP"; " HIGH SCORE", "2UP"
        box_width = width // 3
        # -----------------BOX-----------------------
        # -------------|--------------|--------------
        #       1UP       HIGH SCORE        2UP
        # -------------|--------------|--------------
        # 0       1*box_width     2*box_width     3*box_width
        box = [0, box_width, 2*box_width, 3*box_width]

        # Get the position to place text center
        x_1up = self._get_center_position(box[0], box[1], "1UP") + x_distance
        x_highscore = self._get_center_position(
            box[1], box[2], " HIGH SCORE") + x_distance
        x_2up = self._get_center_position(box[2], box[3], "2UP") + x_distance

        # Add string at the box center
        score = self.level.score
        self.window.addstr(y_distance - 2, x_1up, "1UP")
        self.window.addstr(y_distance - 2, x_highscore, " HIGH SCORE")
        self.window.addstr(y_distance - 2, x_2up, "2UP")
        self.window.addstr(y_distance - 1, box_width //
                           2 + x_distance, f"{score}")
        self.window.addstr(y_distance - 1, 3*box_width //
                           2 + x_distance, f"{score}")
        self.window.addstr(y_distance - 1, 5*box_width // 2 + x_distance, "0")

        # Decoration part
        pacman_color = self._get_pair_number_of_color(COLOR_RGB_PACMAN)
        y_decoration = height + y_distance
        for i in range(0, self.level.lives*2, 2):
            self.window.addstr(
                y_decoration, x_1up + i, "ᗤ", pacman_color)
        self.window.addstr(y_decoration, x_2up + 2, "🍒")

        # Draw ready state
        ready_color = self._get_pair_number_of_color(self.level.ready.color)
        self.window.addstr(
            self.level.ready.y + y_distance,
            self.level.ready.x + x_distance - len(self.level.ready.symbol)//2,
            self.level.ready.symbol, ready_color)

    # Draw Screen 2: Map with Dots and Power Capsule

    def __draw_screen_2(self):
        # Get ingredients
        map_grip = self.level.pmap.pretty_map
        width = self.level.pmap.width  # 28
        height = self.level.pmap.height  # 30
        simple_grip = self.level.pmap.grip
        # Get the heights between map to screen
        y_distance, x_distance = self.__calculate_offset()
        color = ''
        for row in range(height):
            for col in range(width):
                if simple_grip[row][col] == WALL:
                    color = COLOR_RGB_WALL
                    att = self._get_pair_number_of_color(color)
                    self.window.addstr(row + y_distance, col + x_distance,
                                       map_grip[row][col], att)

                elif simple_grip[row][col] == POINTS \
                        or simple_grip[row][col] == ENERGIZER:
                    color = COLOR_RGB_POINTS
                    att = self._get_pair_number_of_color(color)
                    self.window.addstr(row + y_distance, col + x_distance,
                                       map_grip[row][col], att)

    def __get_ghost_color(self, color):
        colors = (
            COLOR_RGB_BLINKY,
            COLOR_RGB_PINKY,
            COLOR_RGB_INKY,
            COLOR_RGB_CLYDE,
            COLOR_RGB_WALL,
            COLOR_RGB_WHITE
        )
        if color in colors:
            return self._get_pair_number_of_color(color)

    # Draw Screen 3: Pac-Man, Ghosts, and Bonus Fruit

    def __draw_screen_3(self):
        # Draw pacman
        self.__draw_pacman()
        # Draw Ghosts
        self.__draw_ghosts()
        if not self.level.ready.state:
            self.__draw_bonus()

    def __draw_pacman(self):
        # Create objects
        pacman = self.level.pacman

        # Get the heights between map to screen
        y_distance, x_distance = self.__calculate_offset()

        pacman_color = self._get_pair_number_of_color(COLOR_RGB_PACMAN)

        # Draw PACMAN
        self.window.addstr(
            pacman.y + y_distance, pacman.x + x_distance, pacman.symbol, pacman_color)

    def __draw_ghosts(self):
        # Create objects
        ghosts_list = self.level.ghosts

        # Get the heights between map to screen
        y_distance, x_distance = self.__calculate_offset()

        # Draw GHOSTS
        for ghost in ghosts_list:
            ghost_color = self.__get_ghost_color(ghost.color)
            self.window.addstr(
                ghost.y + y_distance, ghost.x + x_distance, ghost.symbol, ghost_color)

    def __draw_bonus(self):
        bonuses_list = self.level.bonuses

        # Get the heights between map to screen
        y_distance, x_distance = self.__calculate_offset()

        # Find bonuses object
        for bonus in bonuses_list:
            self.window.addstr(
                bonus.y + y_distance, bonus.x + x_distance, bonus.symbol)

    def __is_fully_visible(self):
        width = self.level.pmap.width
        height = self.level.pmap.height
        # Check if screen was re-sized (True or False)
        is_resize = curses.is_term_resized(height + 3, width + 3)
        return is_resize

    def inform_enlarge_terminal(self):
        maxX, maxY = self.__get_max_width_height()
        width = self.level.pmap.width
        height = self.level.pmap.height
        if maxX <= width + 6 or maxY <= height + 6:
            if self.__is_fully_visible():
                self.window.clear()
                self.window.addstr(1, 0, "Enlarge ... your terminal!")
                # Sleep 0.5 s
                curses.napms(500)

    def get_key_input(self):
        return self.window.getch()

    def __get_max_width_height(self):
        return self.window.getmaxyx()

    def __calculate_offset(self):
        width = self.level.pmap.width
        height = self.level.pmap.height
        maxY, maxX = self.__get_max_width_height()
        x_coordinate = (maxX - width) // 2
        y_coordinate = (maxY - height) // 2

        return y_coordinate, x_coordinate
