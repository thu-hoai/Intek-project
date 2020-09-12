#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build Objects Pacman and Ghost"""

import curses
import random
import copy
import itertools
from pacman.constants import (
    PACMAN, GHOST, COLOR_RGB_PACMAN, READY_STATE,
    COLOR_RGB_BLINKY, COLOR_RGB_PINKY, COLOR_RGB_INKY, COLOR_RGB_CLYDE,
    AVAILABLE_BONUS_POINTS, Directions, GameControls, COLOR_RGB_WALL,
    COLOR_RGB_READY_STATE)


class Object:
    """A class of Characters in Pac Man Game"""

    def __init__(self, x, y, symbol, color):
        """The constructor for Object class
        Arguments:
            x {int} -- Represent to the x-coordinates position of Object
            y {int} -- Represent to the y-coordinates position of Object
            symbol {str} -- The Unicode character that visually represents
                the object
            color {tuple} -- A possible color to display the symbol of
                the object with.
        """
        if not all([isinstance(i, int) for i in (x, y)]):
            raise ValueError(
                "The x-coordinate or y-coordinate must be an integer")
        if color:
            if not isinstance(color, tuple):
                raise ValueError("The color must be a tuple")
            if not all([0 <= i <= 255 for i in color]):
                raise ValueError(
                    "The color must be a tuple of 3-component integer"
                    + '' + " and must be in range 0-255")
        if not isinstance(symbol, str):
            raise ValueError("Symbol must be a string")
        self._x = x
        self._y = y
        self._symbol = symbol
        self._color = color

    @property
    def x(self):
        """Represent to the x-coordinates position of Object"""
        return self._x

    @property
    def y(self):
        """Represent to the y-coordinates position of Object"""
        return self._y

    @property
    def symbol(self):
        """The Unicode character that visually represents the object"""
        return self._symbol

    @property
    def color(self):
        """A possible color to display the symbol of the object with."""
        return self._color

    def __repr__(self):
        return f'{self.__class__.__name__}(x={self.x}, y={self.y}, symbol={self.symbol}, color={self.color}'

    def __eq__(self, other):
        return (self.x, self.y, self.symbol, self.color) == \
            (other.x, other.y, other.symbol, other.color)


class StandingStartAnnouncement(Object):
    def __init__(self, x, y):
        """The constructor of StandingStartAnnouncement """
        super().__init__(x, y, READY_STATE, COLOR_RGB_READY_STATE)
        self.state = True


class AnimatedCharacter(Object):
    """A Class define the animated character"""

    def __init__(self, x, y, symbol, color):
        """The constructor of AnimatedCharacter """
        super().__init__(x, y, symbol, color)

    PACMAN_CONTROLS = {
        curses.KEY_LEFT: (-1, 0),
        curses.KEY_RIGHT: (1, 0),
        curses.KEY_UP: (0, -1),
        curses.KEY_DOWN: (0, 1)
    }

    # Directions
    GHOST_DIRECTION_CONTROLS = {Directions.UP: (0, -1),
                                Directions.RIGHT: (1, 0),
                                Directions.DOWN: (0, 1),
                                Directions.LEFT: (-1, 0)}

    @staticmethod
    # Check if the character move over the boundaries
    def _is_over_the_fence(x, y, width, heigh):
        if x >= width or x <= 0 or y >= heigh or y <= 0:
            return True

    def set_direction(self, dx, dy):
        """ Set the horizontal and the vertical directions which
            the character is moving towards

        Arguments:
            dx {int} -- indicate the horizontal direction which is
                the character moving toward
            dy {inf} -- indicate the vertical direction which is
                the character moving towards

        Raises:
            ValueError: dx, dy both are not integers
            ValueError: dx, dy both are not in [-1, 1]
        """
        if any([not isinstance(i, int) for i in (dx, dy)]):
            raise ValueError("dx, dy must be intergers")
        if not all([-1 <= i <= 1 for i in (dx, dy)]):
            raise ValueError("dx, dy must be in [-1, 1]")

        # Set direction if user pressed any arrow key
        self._x += dx
        self._y += dy

    def play(self, scene, key_code=None):
        """ Updates the current location (coordinates) of the character
            in the maze depending on the current direction the character
            is moving towards.
            If the character hits a wall, the method play stops the character
            and clears the direction that the character
            was moving towards.

        Arguments:
            scene {Scene} -- A Scene Object

        """
        # Get Wall coordinates list
        wall_coordinates = scene.level.pmap.wall_coordinates
        width = scene.level.pmap.width
        height = scene.level.pmap.height

        if key_code:
            # KEY ARROW control - not hit the wall
            # Initialize a list to track the coordinates of the `character`
            character_move_track = []
            character_move_track.append((self.x, self.y))

            # Get the offset if the user press key code
            dx, dy = self.PACMAN_CONTROLS[key_code]

            next_x = self.x + dx
            next_y = self.y + dy

            # Support to pacman cross the gate
            if self._is_over_the_fence(next_x, next_y, width, height) and\
                    (next_y, next_x) not in wall_coordinates:
                offset = Pacman._support_pacman_cross_the_gate(
                    next_x, next_y, width, height)
                (self._x, self._y) = (self._x + offset[0], self._y + offset[1])

            # Check if the next step the character hits a wall or not
            if (next_y, next_x) not in wall_coordinates and\
                    not self._is_over_the_fence(next_x, next_y, width, height):

                # Update coordinates of the character
                self.set_direction(dx, dy)
                character_move_track.pop(0)
                character_move_track.append((self.x, self.y))


class Bonus(Object):
    """A Class define the Bonus - The number of points that the player earns"""

    def __init__(self, x, y, symbol, points):
        """The constructor of Bonus class """

        if not isinstance(points, int):
            raise ValueError("Points must be an integer")
        if symbol in AVAILABLE_BONUS_POINTS:
            if points != AVAILABLE_BONUS_POINTS[symbol]:
                raise ValueError("Points must be appropriate to the symbol")
        self.points = points
        super().__init__(x, y, symbol, color=None)


class Pacman(AnimatedCharacter):
    """A Class define the animated Pacman"""

    def __init__(self, x, y):
        """The constructor of the animated Pacman class """
        super().__init__(x, y, PACMAN, COLOR_RGB_PACMAN)
        self.is_dead = False
        self.can_eat_ghosts = False

    def update_map_when_pacman_move(self, pmap):
        """Update map when pacman move
        Arguments:
            scene {model.Scene}
        """
        # Update the maze when the character eat points
        if (self.y, self.x) in pmap.point_coordinates:
            pmap.grip[self.y][self.x] = ' '

        # Update the maze when the character eat energizers
        elif (self.y, self.x) in pmap.energizer_coordinates:
            pmap.grip[self.y][self.x] = ' '

    @staticmethod
    # Get the offset (dx, dy) which pacman is moving forward
    # in case pacman hits the gate
    def _support_pacman_cross_the_gate(next_x, next_y, width, height):
        if next_x == width:
            return (- width + 1, 0)
        if next_x == 0:
            return (width - 1, 0)
        if next_y == height:
            return (0, - height + 1)
        if next_y == 0:
            return (0, height - 1)


class Ghost(AnimatedCharacter):
    """A Class define the animated Ghost"""

    def __init__(self, x, y, color):
        """The constructor of the animated Ghost class """
        super().__init__(x, y, GHOST, color)
        # Set initial Direction
        self.current_direction = Directions.UP
        # Ghost are not scared as default
        self.is_scared = False
        self.is_eaten = False

    def play(self, scene):
        """ Ghosts Leaving Home and Moving Randomly
            Once a ghost has left home, it chooses a direction to move towards.
                A ghost continues towards this direction until either it hits
                a wall or it arrives at an intersection:

                If a ghost hits a wall, it determines a new direction to
                    move forward.The ghost doesn't choose a direction
                    that lets it move backward to its previous direction.
                If a ghost arrives at an intersection, it chooses whatever
                    direction that doesn't let it move backward to its
                    previous direction.
                If a ghost collides with another ghost, it must go to
                    another direction. If a ghost is blocked by two other
                    ghosts, it must hold on until there is a new available
                    direction for it to go to.
        Arguments:
            scene {Scene} -- A Scene Object
        """
        #       UP ^
        #          |
        # LEFT     |      RIGHT
        # <-----CURRENT---->
        #          |
        #          |
        #          v DOWN
        # Get a list of legal neighbor directions
        legal_neighbor = self._get_legal_neighbor_directions(scene)
        # In case the ghost must move backward
        # ___
        # |X|
        # | |
        # | |
        if legal_neighbor == []:
            direct = self._find_backward_direction(self.current_direction)
        else:
            # Normal cases - get the random direction
            direct = random.choice(legal_neighbor)

        # Move and update current direction
        dx, dy = self.GHOST_DIRECTION_CONTROLS[direct]
        self.set_direction(dx, dy)
        self.current_direction = direct

    # Neighbor directions are called legal if they will:
    # - Not hit the wall
    # - Not move backward
    # - Not over the boundaries
    def _get_legal_neighbor_directions(self, scene):
        # Get ingredients
        wall_coordinates = scene.level.pmap.wall_coordinates
        width = scene.level.pmap.width
        height = scene.level.pmap.height
        # Get backward direction
        backward_direction = self._find_backward_direction(
            self.current_direction)
        # Initialize a list of legal neighbor directions
        legal_neighbors = []

        for direction, step in self.GHOST_DIRECTION_CONTROLS.items():
            # Check possible steps
            dx, dy = step
            next_x = self.x + dx
            next_y = self.y + dy
            # Do not move to backward direction
            if direction == backward_direction:
                continue
            # Do not move to WALL
            if (next_y, next_x) not in wall_coordinates:
                if not self._is_over_the_fence(next_x, next_y, width, height):
                    legal_neighbors.append(direction)

        return legal_neighbors

    @staticmethod
    # Define the direction to not move backward
    def _find_backward_direction(current_direction):
        if current_direction == Directions.UP:
            return Directions.DOWN
        if current_direction == Directions.DOWN:
            return Directions.UP
        if current_direction == Directions.LEFT:
            return Directions.RIGHT
        if current_direction == Directions.RIGHT:
            return Directions.LEFT


class Blinky(Ghost):
    """A Class define the animated Blinky"""

    def __init__(self, x, y):
        """The constructor of the animated Blinky class """
        super().__init__(x, y, COLOR_RGB_BLINKY)

    @staticmethod
    def get_node_object(weighted_list, id_):
        for point in weighted_list:
            if point.id == id_:
                return point

    @staticmethod
    def get_id_list(weighted_list):
        return [point.id for point in weighted_list]


    def play_blinky(self, scene):
        scene.level.pmap._get_weighted_graph()
        weighted_list = scene.level.pmap.weighted_graph
        intersections_id = self.get_id_list(weighted_list)

        # Current pacman id
        pac_x_coord, pac_y_coord = scene.level.pacman.x, scene.level.pacman.y
        pacman_id = pac_y_coord * scene.level.pmap.width + (
            pac_x_coord + pac_y_coord)
        # pacman_point = self.get_node_object(weighted_list, pacman_id)
        nearest_pacman_id = scene.level.pmap.get_the_nearest_intersection(
            (pac_x_coord, pac_y_coord)).id
        pacman = self.get_node_object(weighted_list, nearest_pacman_id)

        # Current Blinky id
        blinky_id = self.y * scene.level.pmap.width + (self.x + self.y)
        nearest_blinky_id = scene.level.pmap.get_the_nearest_intersection(
            (self.x, self.y)).id
        blinky = self.get_node_object(weighted_list, nearest_blinky_id)

        # Find the shortest path
        shortest_path = scene.level.pmap.find_shortest_path(
            blinky, pacman)

        for node in shortest_path:
            self._x, self._y = node.x, node.y


class Pinky(Ghost):
    """A Class define the animated Pinky"""

    def __init__(self, x, y):
        """The constructor of the animated Pinky class """
        super().__init__(x, y, COLOR_RGB_PINKY)


class Inky(Ghost):
    """A Class define the animated Inky"""

    def __init__(self, x, y):
        """The constructor of the animated Inky class """
        super().__init__(x, y, COLOR_RGB_INKY)


class Clyde(Ghost):
    """A Class define the animated Clyde"""

    def __init__(self, x, y):
        """The constructor of the animated Clyde class """
        super().__init__(x, y, COLOR_RGB_CLYDE)
