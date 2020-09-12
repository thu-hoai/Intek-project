#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build Game Engine of Game"""

import time
import copy
import curses
from model.scene import Scene
from model.level import Level
from model.objects import Blinky, Inky, Clyde, Pinky
from pacman.constants import (
    PACMAN, GHOST, COLOR_RGB_CLYDE, COLOR_RGB_INKY, COLOR_RGB_BLINKY,
    COLOR_RGB_PINKY, COLOR_RGB_WALL, COLOR_RGB_WHITE, COLOR_RGB_READY_STATE,
    DEFAULT_BACKGROUND_COLOR, GameControls)


class PacmanGameEngine:
    """"A Class Pac-Man Game Engine"""

    PACMAN_DEAD_TIME = 0
    GHOST_SCARED_TIME = 0
    READY_STATE = 0
    GHOST_EYED_TIME = {Blinky: 0, Pinky: 0, Inky: 0, Clyde: 0}
    GHOSTS_ARE_EATEN = {Blinky: False, Pinky: False, Inky: False, Clyde: False}
    PACMAN_IS_CHASED = 0

    def __init__(self):
        """The constructor of Game Engine """
        self.level = None
        self.scene = None

    @staticmethod
    def __set_up():
        """ Initializes the curses library
        Returns:
            window object -- represents the whole screen.
        """
        # Return a window object which represents the whole screen.
        window = curses.initscr()
        # Leave echo mode. Echoing of input characters is turned off
        curses.noecho()
        # Enter cbreak mode.
        curses.cbreak()
        # Set the cursor state to invisible,
        curses.curs_set(0)
        window.keypad(True)
        window.nodelay(1)
        # Check if change the colors displayed by the terminal.
        if not curses.has_colors() or not curses.can_change_color():
            raise Exception("Your terminal doesn't allow to use colors.")
        return window

    @staticmethod
    def __tear_down(window):
        """Deinitialize the curses library.
            Reverse terminal setting
        """
        # reverse terminal settings
        # # Turn off cbreak mode
        curses.nocbreak()
        # Turn echo back on
        curses.echo()
        # Turn cursor back on
        curses.curs_set(1)
        # Turn off keypad keys
        window.keypad(False)
        window.nodelay(0)
        # De-initialize the library, and return terminal to normal status.
        curses.endwin()

    def __run(self):
        """Implement the game logic"""

        # Set some Initial value
        direction = ''   # Direction as key of pacman
        key = ''         # The key which is input
        sleep_time = 0   # Time we sleep each turn through the game loop
        count = 0
        pacman = self.scene.level.pacman
        pacman_start_coordinate = (pacman.x, pacman.y)
        is_game_running = True
        self.__on_start_ready_state_time()

        while is_game_running:
            # Get start time of each turn through the game loop
            start_time = time.time()
            count += 1

            # INPUT CONTROLS
            # =======================================================
            if not self.level.ready.state:
                key = self.scene.get_key_input()
            # Set direction if user pressed any arrow key
            if key in pacman.PACMAN_CONTROLS:
                direction = key
            if not pacman.is_dead:
                pacman.play(self.scene, direction)

            # UPDATE
            # =======================================================
            self.update(count, pacman_start_coordinate)

            # RENDER SCREEN
            # =======================================================
            if key == curses.KEY_RESIZE:
                self.scene.inform_enlarge_terminal()
            else:
                self.scene.render()

            # END GAME
            # =======================================================
            if key == GameControls.QUIT_KEY or self.__is_end_game():
                is_game_running = False

            # GAME SPEED CONTROLS
            # ======================================================
            sleep_time = start_time +\
                GameControls.MS_PER_FRAME/1000 - time.time()
            if sleep_time >= 0:
                # Flush all input buffers
                curses.flushinp()
                time.sleep(sleep_time)

    def start(self, level_number):
        """Call game
        Arguments:
            level_number {int} -- the level/map to load
        """
        if not isinstance(level_number, int):
            raise ValueError("Provided level number must be an integer")

        # Initialize the screen and set up
        window = self.__set_up()

        # Get ingredients
        self.level = Level.load(level_number)
        self.scene = Scene(window, self.level)
        try:
            self.__run()
        finally:
            # Return terminal to normal status.
            self.__tear_down(window)

    def update(self, count, pacman_start_coordinate):
        """Update all events in game"""
        # Get ingredients
        pacman = self.scene.level.pacman
        ghosts_list = self.scene.level.ghosts
        energizer_deep_copy = copy.deepcopy(
            self.level.pmap.energizer_coordinates)

        # Ready state Duration
        if self.level.ready.state:
            if self.__is_ready_state_ended():
                self.level.ready.state = False
            else:
                self.__change_ready_state(count)

        # Play pacman and ghosts after READY duration
        if not self.level.ready.state:
            if not pacman.is_dead:
                pacman.update_map_when_pacman_move(self.scene.level.pmap)
            for ghost in ghosts_list:
                ghost.play(self.scene)
                if isinstance(ghost, Blinky) and \
                    self.__is_blinky_start_chase_pacman():
                    ghost.play_blinky(self.scene)

        # Define which is the next step if there's a collision
        # Set pacman.is_dead and pacman.can_eat_ghosts
        self.__resolve_collisions(energizer_deep_copy)

        # Decide actions if ghost turns vulnerable and pacman can eat ghost
        if pacman.can_eat_ghosts:
            if not pacman.is_dead:
                self.__change_vulnerable_ghosts_to_eyes()
            if self.__is_blue_ghosts_ended():
                for ghost in ghosts_list:
                    ghost._color = COLOR_RGB_WALL
            else:
                self.__change_color_ghosts_flashed(count)
            if self.__is_scared_ghosts_ended():
                self.__change_scared_ghosts_to_normal()
                pacman.can_eat_ghosts = False

        # Decide actions if pacman loses his life
        if pacman.is_dead:
            if self.__is_pacman_dead_time_ended():
                # Update pacman coordinates at his initial location
                pacman._x, pacman._y = pacman_start_coordinate
                pacman._symbol = PACMAN
                pacman.is_dead = False
            else:
                self.__change_symbol_pacman_flashed(count)

        # Decide actions if there's a ghost is eaten by pacman
        if self.__is_any_ghosts_eaten():
            self.__change_ghost_eyes_to_normal()

        # Update score after all
        self.level.update_score()

    def __resolve_collisions(self, energizer_deep_copy):
        pacman = self.scene.level.pacman
        if not pacman.is_dead:
            # Normal case: Pacman is dead
            if not pacman.can_eat_ghosts:
                if self.__is_pacman_touching_ghosts():
                    self.__on_start_pacman_dead_time()
                    pacman.is_dead = True
                    # Update Pacman lives until all lives are lost
                    self.level.lives -= 1
                # If pacman hits energizer: Pacman can eat ghosts
                # (Ghosts are vulnerable (blue or white color))
                if self.__is_pacman_touching_energizer(energizer_deep_copy):
                    energizer_deep_copy.remove((pacman.y, pacman.x))
                    self.__on_start_scared_ghosts_time()
                    pacman.can_eat_ghosts = True

    ####################################################################
    # UPDATE CHARACTERS

    def __change_ready_state(self, count):
        ready_state = self.level.ready
        if count % 2 == 0:
            ready_state._color = DEFAULT_BACKGROUND_COLOR
        else:
            ready_state._color = COLOR_RGB_READY_STATE

    def __change_vulnerable_ghosts_to_eyes(self):
        pacman = self.scene.level.pacman
        ghosts_list = self.scene.level.ghosts
        # Ghosts control: change eyes icon
        for ghost in ghosts_list:
            if (ghost.x, ghost.y) == (pacman.x, pacman.y):
                for obj in (Blinky, Inky, Pinky, Clyde):
                    if isinstance(ghost, obj):
                        self.GHOSTS_ARE_EATEN[obj] = True
                        self.GHOST_EYED_TIME[obj] = time.time()
                ghost.is_eaten = True
                ghost._symbol = GameControls.EYES

    def __change_symbol_pacman_flashed(self, count):
        pacman = self.scene.level.pacman
        if count % 2 == 0:
            pacman._symbol = GameControls.COLLISION
        else:
            pacman._symbol = GameControls.SKULL

    def __change_color_ghosts_flashed(self, count):
        ghosts_list = self.scene.level.ghosts
        if count % 2 == 0:
            for ghost in ghosts_list:
                ghost._color = COLOR_RGB_WALL
        else:
            for ghost in ghosts_list:
                ghost._color = COLOR_RGB_WHITE

    def __change_ghost_eyes_to_normal(self):
        ghosts_list = self.scene.level.ghosts
        for ghost in ghosts_list:
            for obj in (Blinky, Inky, Pinky, Clyde):
                if isinstance(ghost, obj) and self.GHOSTS_ARE_EATEN[obj]\
                    and (time.time() - self.GHOST_EYED_TIME[obj]) >= \
                        GameControls.GHOST_EYES_DURATION:
                    ghost._symbol = GHOST

    def __change_scared_ghosts_to_normal(self):
        ghosts_list = self.scene.level.ghosts
        for ghost in ghosts_list:
            if isinstance(ghost, Blinky):
                ghost._color = COLOR_RGB_BLINKY
            elif isinstance(ghost, Inky):
                ghost._color = COLOR_RGB_INKY
            elif isinstance(ghost, Pinky):
                ghost._color = COLOR_RGB_PINKY
            elif isinstance(ghost, Clyde):
                ghost._color = COLOR_RGB_CLYDE

    ##############################################################
    # TIME MANAGEMENT
    def __on_start_ready_state_time(self):
        current_time = time.time()
        self.READY_STATE = current_time
        self.PACMAN_IS_CHASED = current_time

    def __on_start_pacman_dead_time(self):
        current_time = time.time()
        self.PACMAN_DEAD_TIME = current_time

    def __on_start_scared_ghosts_time(self):
        current_time = time.time()
        self.GHOST_SCARED_TIME = current_time

    @staticmethod
    def __calculate_elapsed_time(start_time):
        return time.time() - start_time

    def __is_blue_ghosts_ended(self):
        return self.__calculate_elapsed_time(self.GHOST_SCARED_TIME)\
            <= GameControls.GHOSTS_BLUE_DURATION

    def __is_pacman_touching_energizer(self, energizer_deep_copy):
        pacman = self.scene.level.pacman
        if (pacman.y, pacman.x) in energizer_deep_copy:
            return True
        return False

    def __is_ready_state_ended(self):
        return self.__calculate_elapsed_time(self.READY_STATE)\
            >= GameControls.READY_STATE_DURATION

    def __is_pacman_dead_time_ended(self):
        return self.__calculate_elapsed_time(self.PACMAN_DEAD_TIME)\
            >= GameControls.PACMAN_DEAD_DURATION

    def __is_scared_ghosts_ended(self):
        return self.__calculate_elapsed_time(self.GHOST_SCARED_TIME) >= \
            GameControls.GHOSTS_SCARED_DURATION

    def __is_blinky_start_chase_pacman(self):
        return self.__calculate_elapsed_time(self.PACMAN_IS_CHASED) >= \
            GameControls.BLINKY_CHASE_PACMAN

    ################################################################
    # CHECK CONDITION
    def __is_end_game(self):
        points_list = self.level.pmap.point_coordinates
        energizer_list = self.level.pmap.energizer_coordinates
        bonus_list = self.level.bonuses
        if self.level.lives == 0:
            return True
        if all([len(lst) == 0 for lst in (
                energizer_list, bonus_list, points_list)]):
            return True

    def __is_any_ghosts_eaten(self):
        for value in self.GHOSTS_ARE_EATEN.values():
            if value:
                return True
        return False

    def __is_pacman_touching_ghosts(self):
        pacman = self.scene.level.pacman
        ghosts_list = self.scene.level.ghosts
        return any([(ghost.x, ghost.y) == (pacman.x, pacman.y)
                    for ghost in ghosts_list])
