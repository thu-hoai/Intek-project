#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build Object Pacman and Ghosts"""
import os.path
import json
import curses
from pacman.constants import COLOR_NUMBER_DICT, DEFAULT_BACKGROUND_COLOR


class Palette:
    """
    A palette that defines a set of composite colors that needs to be
        declared first.
    A composite color is a color with a foreground and a background colors.
    """

    def get_composite_color(
            self, foreground_color, background_color=DEFAULT_BACKGROUND_COLOR):
        """ The curse attribute representing this composite color
        Arguments:
            foreground_color {tuple} -- A foreground color corresponding to
                a tuple (r, g, b) that represents the value of the components
                R, G, and B that range between 0 and 255
            background_color {tuple} -- A background color corresponding to
                a tuple (r, g, b) that represents the value of the components
                R, G, and B that range between 0 and 255.
        Returns:
            The `curse` attribute representing this composite color.
        """

        # Convert RGB colors of the characters to `curses` color
        curses_color = self.__convert_rgb_to_1000(foreground_color)

        # Define and register the colors of the characters
        color_number = COLOR_NUMBER_DICT[foreground_color]
        curses.init_color(color_number,
                          curses_color[0], curses_color[1], curses_color[2])

        # Re-define background color if it is not a default color
        curses.init_color(
                0,
                background_color[0], background_color[1], background_color[2])

        # Definde color pair for each of character (start with 1)
        curses.init_pair(
            COLOR_NUMBER_DICT[foreground_color] - 7,
            color_number,
            curses.COLOR_BLACK)
        try:
            # Complete register the colors
            # Return the attribute value for displaying characters
            curses.color_pair(color_number)
        except curses.error:
            pass
        # Return attribute representing the composite color.
        return (COLOR_NUMBER_DICT[foreground_color]-7) * 256

    @staticmethod
    # Convert RGB color to curses band
    def __convert_rgb_to_1000(rgb_color):
        lst = [int(round(i*1000/255)) for i in rgb_color]
        return tuple(lst)
