#!/usr/bin/env python3
import csv
import datetime
import argparse
import os

# Manage column index of csv data
CSV_FORMAT = {
    'MATCH_TIME': 0,
    'PLAYER1_NAME': 1, 'PLAYER2_NAME': 4,
    'PLAYER1_POINT': 2, 'PLAYER2_POINT': 3
}

# The actual score for win
WIN = 1
# The actual score for draw
DRAW = 0.5
# The actual score for loss
LOST = 0
# Default Elo K-factor
K_FACTOR = 32
# Default rating
INITIAL_RATING = 0.0


# Waypoint 1: Class Player
class Player:
    """ Class Player that represents a player and his current Elo rating """

    def __init__(self, name, rating=INITIAL_RATING):
        """ The constructor for Player class

        Parameters:
            name (str): name of player
            rating (float): the initial Elo rating of the player
                (0 if not defined)
        """
        self.__name = name
        self.__rating = rating

    @property
    def name(self):
        """ The name of player """
        return self.__name

    @property
    def rating(self):
        """ Elo rating of the player """
        return self.__rating

    @rating.setter
    def rating(self, value):
        """Set rating"""
        self.__rating = float(value)

    # Waypoint 6: Expected Score Calculation
    def calculate_expected_score(self, opponent):
        """ Return the expected Elo score of the player
            if he were competing against the other player

        Parameter: opponent: object Player representing a opponent

        Returns: The expected Elo score of the player
        """
        return 1 / (1 + 10 ** ((opponent.rating - self.rating) / 400))


# Waypoint 2: Class MatchResult
class MatchResult:
    """Class MatchResult represents a match that occurred between two players"""

    def __init__(self, match_time, player1, player2, player1_points, player2_points):
        """ The constructor for MatchResult class

        Parameters:
            match_time (str): the date when the match occurred.
            player1: objects Player referring to the first player.
            player2: objects Player referring to second player.
            player1_points (int): the number of points of the first player
            player2_points (int): the number of points of the first player
        """
        # Data validation
        # Distint players one match
        if player1 == player2:
            raise ValueError('Must be distinct players')
        # Points must be integers
        if not all([isinstance(x, int) for x in (player1_points, player2_points)]):
            raise ValueError('Points must be integers')

        self.__match_time = self.__format_match_time(match_time)
        self.__player1 = player1
        self.__player2 = player2
        self.__player1_points = player1_points
        self.__player2_points = player2_points

    @staticmethod
    def __format_match_time(date_time):
        """ Format match_time as '%Y-%m-%d'

        Parameter: date_time (str): string represent date time as YYYY-MM-DD

        Return: an object datetime
        """

        return datetime.datetime.strptime(date_time, '%Y-%m-%d')

    @property
    def match_time(self):
        """Time of each match"""
        return self.__match_time

    @property
    def player1(self):
        """Name of the player"""
        return self.__player1

    @property
    def player2(self):
        """Name of the player"""
        return self.__player2

    @property
    def player1_points(self):
        """Points of the player"""
        return self.__player1_points

    @property
    def player2_points(self):
        """Points of the player"""
        return self.__player2_points


# Waypoint 3: Match Result CSV File Import
def read_match_results(csv_file_path_name):
    """Return a list of object from a CSV file

    Parameters:
        csv_file_path_name (str): path and name of a CSV file

    Return:
        a list of objects MatchResults built with the data
            parsed from the file csv_file_path_name
    """

    # Initialize a dictionary store instances players
    player_object = {}

    # Initialize a list store list of objects match result
    match_list = []

    with open(csv_file_path_name, 'r') as csvfile:
        reader = csv.reader(csvfile)
        # Sorted by match_time
        sortedlist = sorted(reader, key=lambda row: row[CSV_FORMAT['MATCH_TIME']],
                            reverse=False)
        # Read line by line
        for row in sortedlist:
            # Get a dic with key is the names of player and value is an object
            player_object.setdefault(row[CSV_FORMAT['PLAYER1_NAME']],
                                     Player(row[CSV_FORMAT['PLAYER1_NAME']]))
            player_object.setdefault(row[CSV_FORMAT['PLAYER2_NAME']],
                                     Player(row[CSV_FORMAT['PLAYER2_NAME']]))
            # Identify and add MatchResult object each line
            match_list.append(MatchResult(
                row[CSV_FORMAT['MATCH_TIME']],
                player_object[row[CSV_FORMAT['PLAYER1_NAME']]],
                player_object[row[CSV_FORMAT['PLAYER2_NAME']]],
                int(row[CSV_FORMAT['PLAYER1_POINT']]),
                int(row[CSV_FORMAT['PLAYER2_POINT']])))

    return match_list


# Waypoint 4 & 5 Command-Line Interface Script
def parse_arguments():
    """Convert argument strings to objects and assign them as attributes of
    the namespace.

    Return: an instance ``argparse.Namespace`` corresponding to the
        populated namespace.
    """
    # Initialize parser
    parser = argparse.ArgumentParser(description='Elo Rating')

    # Add positional and optional arguments
    parser.add_argument('-f', '--file', metavar='FILE', required=True,
                        help='The path of the CSV file containing\
                            results of matches between players')

    parser.add_argument('-a', '--advanced-calculation', required=False,
                        action="store_true",
                        help='The advanced Elo rating based\
                        on the players point difference in a match')

    return parser.parse_args()


# Waypoint 7: Match Outcome Player Score Calculation
def calculate_match_outcome_player_score(
        player_points,
        opponent_points,
        advanced_calculation=False):
    """ Calculate score of the player in a match

    Args:
        param player_points (int): the points that a player
        param opponent_points (int): the points that his opponent

    Keyword Args: advanced_calculation (bool)(default: {False})
        If False, uses the classic Elo rating calculation.
        If True, uses advanced calculation method.

    Returns:
    advanced_calculation=False
        The score of the player player
    """
    # Data validation
    if not all([isinstance(point, int) for point in (player_points, opponent_points)]):
        raise ValueError('Points must be integers')
    
    # Uses advanced calculation method (WP11)
    if advanced_calculation:
        return player_points/(player_points + opponent_points)

    # Uses the classic Elo rating calculation
    # In case the player won against the opponent
    if player_points > opponent_points:
        return WIN

    # In case the player won against the opponent
    if player_points < opponent_points:
        return LOST

    # In case the game is a draw
    return DRAW


# Waypoint 8: Player Rating Update Calculation
def calculate_player_updated_elo_rating(
        player, opponent, player_points, opponent_points, K=K_FACTOR):
    """Return new Elo rating of the player

    Arguments:
        player: An object Player representing a player.
        opponent: An object Player representing an opponent.
        player_points: The points won by the player during a match.
        opponent_points: The points won by the opponent during this same match.

    Keyword Arguments:
        K: The value of the Elo K-factor to use (default: {K_FACTOR})

    Returns:
        the new Elo rating of the player
    """
    # Data validation
    if player == opponent:
        raise ValueError('Must be distinct players')

    if not all([isinstance(points, int) for points in (player_points, opponent_points)]):
        raise ValueError('Points must be integers')

    # Calculate the Elo rating by fomular rA + K(real_score - expected score)
    return player.rating + K * (
        calculate_match_outcome_player_score(
            player_points, opponent_points, parse_arguments().advanced_calculation)
        - player.calculate_expected_score(opponent))


# Waypoint 9: Player Rating Update
def update_player_elo_ratings(match_result):
    """ Updates the Elo rating of two players depending on
        the outcome of the match they played together.

    Parameter: match_result: object MatchResult
    """
    # Updates the Elo rating at the same time
    (match_result.player1.rating, match_result.player2.rating) = (
        calculate_player_updated_elo_rating(
            match_result.player1,
            match_result.player2,
            match_result.player1_points,
            match_result.player2_points,
            K=K_FACTOR),
        calculate_player_updated_elo_rating(
            match_result.player2,
            match_result.player1,
            match_result.player2_points,
            match_result.player1_points,
            K=K_FACTOR))


# Waypoint 10: Match Results Processing
def process_match_results(match_results):
    """ Updates the Elo rating of the players

    Parameter: match_result: object MatchResult
    """
    # Update Elo rating by evoke func update elo each match
    for match_result in match_results:
        update_player_elo_ratings(match_result)


def main():
    """
    Demonstrate and running
    """
    arguments = parse_arguments()

    # Get absolute path of file csv
    abs_path = os.path.abspath(os.path.expanduser(arguments.file))

    # Check if exist path name
    if not os.path.exists(abs_path):
        raise TypeError("Not a exist path")

    # Check if give file is csv format or not
    if not arguments.file.endswith(".csv"):
        raise TypeError("Not a csv file")
    
    # Read match results from given file
    match_results = read_match_results(arguments.file)


    # TEST FOR WAYPOINT 10
    process_match_results(match_results)
    players = set()
    for match_result in match_results:
        players.add(match_result.player1)
        players.add(match_result.player2)
    for rank, player in enumerate(sorted(players,
                                         key=lambda player: player.rating, 
                                         reverse=True), start=1):
        print(f"{rank}. {player.name} ({round(player.rating, 2)})")


if __name__ == "__main__":
    main()
