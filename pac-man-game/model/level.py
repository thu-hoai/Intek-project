#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build Level of Game"""
import os.path
import json
from model.objects import (
    Pacman, Bonus, Blinky, Pinky, Inky, Clyde, StandingStartAnnouncement)
from model.map import Map
from pacman.constants import AVAILABLE_BONUSES_LIST, GHOSTS_LIST, GameControls

# Get path running script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
MAP_DIR = os.path.join(BASE_DIR, 'map')


class Level:
    """A class represent to a secsion of Pacman game"""

    def __init__(self, number, pmap, objects):
        """The constructor of Game Level Class
        Parameters:
            pmap {model.Map Object} -- The object map in particular level
            objects {list} -- A list of objects which class inherited
                from `Object`
            number {int} -- representing the level to load.
                Level number starts with default: {INITIAL_LEVEL}
        Raises:
            Exception: call directly the constructor of the class `Level`
        """
        if self.__class__.__name__ == Level.__name__:
            raise Exception(
                f"The Class {self.__class__.__name__} must be instantiated with its factory methods")

        self.number = number
        self.pmap = pmap
        self.objects = objects
        objects_dict = self.__get_objects_dictionary(number)
        self.pacman = objects_dict['pacman']
        self.ghosts = objects_dict['ghosts']
        self.bonuses = objects_dict['bonuses']
        self.ready = objects_dict['standing_start_announcement']
        self.score = GameControls.INITIAL_SCORE
        self.lives = GameControls.LIVES

    @staticmethod
    def __build_level(number, pmap, objects):
        class __LevelImpl(Level):
            def __init__(self, number, pmap, objects):
                super().__init__(number, pmap, objects)
        return __LevelImpl(number, pmap, objects)

    @classmethod
    def load(cls, number, root_path_name=MAP_DIR):
        """Load Game Level
        Arguments:
            number {int} -- An integer representing the level to load.
                Level number starts with 0.
        Keyword Arguments:
            root_path_name {str} -- Path of the root directory where
                Pac-Man game is stored in. (default: {None})
        Raises:
            ValueError: Provided level number must be an integer
            ValueError: Provided file path name must be an string
            FileNotFoundError: File map is not found
        Returns:
            A Level Object
        """
        if not isinstance(number, int):
            raise ValueError("Provided number must be an integer")
        if root_path_name:
            if not isinstance(root_path_name, str):
                raise ValueError("Provided file path name must be an string")
        # Get file path name of particular map
        map_file_pathname = os.path.join(MAP_DIR, f'level{number}.map')
        if not os.path.exists(map_file_pathname):
            raise FileNotFoundError(f'level{number}.map is not found')
        # Create pacman object
        pmap = Map.load_map(map_file_pathname)
        # Get a dictionary of objects which class inherited from `Object`
        objects_dict = cls.__get_objects_dictionary(number)
        objects = objects_dict.values()
        return cls.__build_level(number, pmap, objects)

    @staticmethod
    def __get_objects_dictionary(number):
        # Initialize an dictionary with `pacman`, `ghosts`, `bonuses`
        # is key resquectively and value is a list of object
        objects_dict = {}
        file_pathname = os.path.join(MAP_DIR, f'level{number}.json')
        if not os.path.exists(file_pathname):
            raise FileNotFoundError(f'level{number}.map is not found')
        # Open the file back and read the contents
        with open(file_pathname) as jsonfile:
            data = json.load(jsonfile)

        # Loop data from json file to add key(str) and value(list of oject)
        # to dictionary
        for character, info in data.items():
            if character == 'pacman':
                pacman = Pacman(info['x'], info['y'])
                objects_dict['pacman'] = pacman
            elif character in GHOSTS_LIST:
                obj = character.capitalize()
                constructor = globals()[obj]
                character_object = constructor(info['x'], info['y'])
                objects_dict.setdefault('ghosts', []).append(character_object)
            elif character in AVAILABLE_BONUSES_LIST:
                bonus_object = Bonus(
                    info[0]['x'], info[0]['y'],
                    info[0]['symbol'], info[0]['points']
                )
                objects_dict.setdefault('bonuses', []).append(bonus_object)
            elif character == 'standing_start_announcement':
                ready_state = StandingStartAnnouncement(info['x'], info['y'])
                objects_dict['standing_start_announcement'] = ready_state

        return objects_dict

    def update_score(self):
        """Update score in game"""
        # Update the maze when the character eat points
        pacman_coord = (self.pacman.y, self.pacman.x)
        if pacman_coord in self.pmap.point_coordinates:
            # Update scores
            self.score += 10
            self.pmap.point_coordinates.remove(pacman_coord)

        if pacman_coord in self.pmap.energizer_coordinates:
            # Update scores
            self.score += 50
            # Eliminate that energize to avoid recalculating score
            self.pmap.energizer_coordinates.remove(pacman_coord)

        # Update the maze when the character eat bonus
        for bonus in self.bonuses:
            if pacman_coord == (bonus.y, bonus.x):
                self.score += bonus.points
                self.bonuses.remove(bonus)

        # Update score: Pacman eat ghosts
        count = 0
        if self.pacman.can_eat_ghosts:
            if any([(ghost.x, ghost.y) == (self.pacman.x, self.pacman.y)
                    for ghost in self.ghosts]):
                count += 1
                self.score += GameControls.EATEN_GHOST_POINTS[count]
