#!/usr/bin/env python3
""" Manage GameSession"""
from game import GameSession
from exception import GameSessionAlreadyExistException

class GameEngine:
    """ A class that represents the controller of
        all the Tiến Lên game sessions that will be created."""

    def create_game_session(self, name):
        """Create a GameSession object

        Arguments:
            name: (str) name of game session

        Raises:
            ValueError: given name is not a string
            GameSessionAlreadyExistException: if game session name existed

        Returns: A GameSession object
        """
        # Raise Error if given name is not a string
        if not isinstance(name, str):
            raise ValueError("Given name is not a string")

        # Raise Error if game session name existed
        if name in GameSession.game_sessions_list:
            raise GameSessionAlreadyExistException(
                f"The game session {GameSession(name).name} already exists")

        # Add name to game_sessions_list if it doesn't exist
        GameSession.game_sessions_list.append(name)

        return GameSession(name)
