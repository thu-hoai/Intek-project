#!/usr/bin/env python3
"""Exception of Game"""
class GameSessionException(Exception):
    """An exception specific to GameSession"""



class PlayerHasAlreadyJoinedException(GameSessionException):
    """An exception specific to GameSession"""



class NoSeatLeftException(GameSessionException):
    """An exception specific to GameSession"""



class GameSessionAlreadyExistException(Exception):
    """An exception specific to GameSession"""


class OnlyOnePlayerJoin(GameSessionException):
    """An exception specific to GameSession"""
