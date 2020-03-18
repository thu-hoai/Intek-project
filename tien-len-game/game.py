#!/usr/bin/env python3
"""Build Tien Len Game"""
import logging
from abc import ABC, abstractmethod
from majormode.utils.namegen import NameGeneratorFactory
from exception import *
from tienlencard import *
from tienlentrick import TienLenTrick


# Set logging
logging.basicConfig(level=logging.INFO, filemode='w')

class Player(ABC):
    """A class Player that represents a player"""

    def __init__(self, name):
        """ The constructor for Player class
        Parameters:
            name: name of player
        """
        self.__name = self.standard_name(name)
        # Keep track of all the game session the player join
        self._player_sessions = []


    @staticmethod
    def standard_name(name):
        """Check valid name and return a standard name
        Arguments:
            name (str): name of the player
        Returns:
            A name which is removed leading and trailling whitespace characters  and
                and any duplicated whitespace characters between words.
        """
        if not isinstance(name, str):
            return ValueError("Not a string")
        return " ".join(name.split())

    @property
    def name(self):
        """Name of a player"""
        return self.__name


    # Waypoint 26: Joining a Game Session (2)
    def join_game_session(self, game_session):
        """ Calls the method join of the object game_session
            that returns an object PlayerSession
        Arguments:
            game_session: an object GameSesion
        """
        self._player_sessions.append(game_session.join(self))
        return

    # Waypoint 29: Event on_cards_dealt
    def on_cards_dealt(self, game_session, cards):
        """ Invoked when a game session starts.
            This event is sent to the players who have joined the game session.
        Arguments:
            player_session: An object PlayerSession that references
                to the game session for which this event occurs.
            cards: A list of object Card that are dealt to the player.
        """
        logging.info("Start by dealing out following cards to %s at %s", self.name,game_session.name)

    def on_player_joined(self, game_session, player):
        """ Invoked when a player joins a game session.
            This event is sent to the players who have already joined the game session.
            This event provides a reference to the player who just joined the game session.
        Arguments:
            player_session: an object PlayerSession that references
                the game session for which this event occurs
            player: an object Player that references the player
                who just joined the game session
        """

        logging.info("%s is already to join %s", player.name, game_session.name)


    def on_game_started(self, game_session):
        """ Invoked when a game session starts.
            This event is sent to the players who have joined the game session.
        Arguments:
            player_session: an object PlayerSession that references
                the game session for which this event occurs)
        """

        logging.info('%s Please be informed game started at %s', self.name, game_session.name)


    def on_round_started(self, game_session):
        """ Invoked when a new round starts in a game session.
            This event is sent to the players who have joined the game session.
            This event provides the round number within the current game session
        Arguments:
            player_session: n object PlayerSession that references
                the game session for which this event occurs)
        """
        logging.info('%s - ROUND started at %s', self.name, game_session.name)

    def on_game_ended(self, game_session, winner):
        """ Invoked when a game session ends.
            This event is sent to the players who have joined the game session.
            This event provides a reference to the player who won the game session.
        Arguments:
            player_session: an object PlayerSession that references
                the game session for which this event occurs)
            winner: an object Player that references the player
                who won the game session
        """
        logging.info('%s - END GAME. The winner is %s in %s', self.name, winner.name, game_session.name)

    def on_round_ended(self, game_session, winner):
        """Invoked when a round of a game session ends.
            This event is sent to the players who have joined the game session.
            This event provides a reference of the player who this round.
        Arguments:
            player_session: an object PlayerSession that references
                the game session for which this event occurs)
            winner: an object Player that references the player
                who won the round of the game session
        """
        logging.info('%s - END ROUND. The winner of round is %s in %s', self.name, winner.name, game_session.name)


    def on_player_in_turn(self, game_session, current_player):
        """Invoked when this is the turn of a player (current player) to play some cards.
            This event is sent to the players who have joined the game session.
            This event provides a reference of the player who needs to play (or pass).
            At this particular time, the current player needs to play some cards.
        Arguments:
            player_session: an object PlayerSession
                that references the game session for which this event occurs
            current_player: an object Player that references the player who is in turn
        """

        logging.info("%s. This is %s's turn", self.name, current_player.name)

    def on_cards_played(self, game_session, cards):
        """Invoked when the current player plays some cards.
            This event is sent to the players who have joined the game session.
            This event provides a reference to the current player
            and the list of the cards that have been played.
        Arguments:
            player_session: an object PlayerSession that references the game session
                for which this event occurs
            cards: a list of object Cards that the current player has played
        """
        logging.info("%s is already dealt by %s at %s", card, self.name, game_session.name)

    def on_player_passed(self, game_session, cards):
        """ Invoke when the current player passes his turn.
            This event is sent to the players who have joined the game session,
            except the current player that passed his turn.
            This event provides a reference to the current player.
        Arguments:
            player_session: an object PlayerSession that references the game session
                for which this event occurs
            cards: a list of object Cards that the current player has played
        """
        logging.info("Already passed. The current card is %s", cards)

    @abstractmethod
    def play(self, game_session):
        pass


# Waypoint 20: Class PC
class PC(Player):
    """A class that inherits from the parent class Player. """
    # Waypoint 35: Method play Implementation for Player Character (PC)
    def play(self, game_session):
        """ Returns an object TienLenTrick that represents the cards
            the player would like to play, or None if the player prefers to pass.
        Arguments:
            game_session: an object GameSession
        """
        # List of card of each player
        player_cards_list = game_session.player_cards
        print()
        logging.info("%s Your turn! Input your cards", self.name)

        # Convert to format to display
        print(" ".join([x.symbol for x in sorted(player_cards_list[self])]))

        tienlen_card_input = None
        # Loop until the player respect requirements
        respect_requirements = True
        while respect_requirements:
            try:
                cards_input = input("Enter the cards separated with spaces: ")

                # In case the player skips his turn
                if cards_input == "pass":
                    return None

                # Convert cards_input to list of object TienLenCard
                cards_list = [TienLenCard(x) for x in cards_input.split(" ")]

                # In case given cards do not match list of card
                if all([i != j for i in cards_list for j in player_cards_list[self]]):
                    logging.warning("You might be kidding! You don't have the card %s", cards_input)
                    continue

                # In case cards input list does not correspond to any valid TienLen trick
                try:
                    tienlen_card_input = TienLenTrick.build_trick(cards_list)
                except:
                    logging.warning("Dude, what trick is that %s ?", cards_input)
                    continue

                # In case the player respect requirements
                respect_requirements = False
            except:
                logging.warning("Dude, %s does not conform with TienLenCard", cards_input)
                pass
        return tienlen_card_input


class NPC(Player):
    """A class that inherits from the parent class Player. """

    __name_generator = NameGeneratorFactory.get_instance(
        NameGeneratorFactory.Language.Japanese)

    def __init__(self):
        super().__init__(self.__name_generator.generate_name())


    def play(self, game_session):
        pass

# Waypoint 23: Class PlayerSession
class PlayerSession:
    """ Represent the session of a player who joins a Tiến Lên game."""

    def __init__(self, player, game_session):
        """The constructor of class PlayerSession
        Parameters:
            player: An object that references the player who is joining a game session.
            game_session: An object that references the game session
                that a player is joining.
        """
        self.__player = player
        self.__game_session = game_session

    @property
    def player(self):
        """ The player who is joining a game session"""
        return self.__player

    @property
    def game_session(self):
        """ The game session that a player is joining"""
        return self.__game_session


class GameSession:
    """ Represent a session of a Tiến Lên game between players"""

    # A list of names of game session
    game_sessions_list = []

    def __init__(self, name):
        """A constructor of GameSession
        Parameter: name: name of game session
        """
        self.__name = name
        # A list of players in GameSession
        self.players = []
        # A dict with keys are player objects and values are the cards they hold
        self.player_cards = {}
        # Store players in one round
        self.players_in_round = []
        # Store players in each Session
        self.players_in_session = []


    @property
    def name(self):
        """Name of game session"""
        return self.__name

    # Waypoint 24: Joining a Game Session (1)
    def join(self, player):
        """Return the player joining the game session
        Arguments:
            player: object references the player who is joining a game session
        Returns:
            An object PlayerSession corresponding to the player joining the game session
        """

        # Raise error if given player exists
        if player in self.players:
            raise PlayerHasAlreadyJoinedException(
                f"The player {player.name} has already joined this game session")
        # Raise error if this GameSession is full
        if len(self.players) == 4:
            raise NoSeatLeftException("All the seats are already occupied")
        # Update players list in this GameSession
        self.players.append(player)
        return PlayerSession(player, self)

    def __process_new_round(self):
        """ Processes new round. Take the players in round under control """
        # Reset every new round
        self.players_in_round = []
        # Start round by add all players in round
        for player in self.players:
            if player:
                self.players_in_round.append([player, True])

    def __process_new_session(self):
        """ Processes new session. Take the players in session under control """
        # Reset every new game
        self.players_in_session = []
        # Start round by add all players in game
        for player in self.players:
            if player:
                self.players_in_session.append(player)

    def __notify_events(self, method, args=None):
        """Observer"""
        for player in self.players:
            if args is None:
                getattr(player, method)(self)
            elif callable(args):
                getattr(player, method)(self, args(player))
            else:
                getattr(player,method)(self, args)

    def __get_card_of_each_player(self, player):
        """Return a list of cards of the given player

        Arguments:  player: oject as a key in player_cards dict

        Returns: a list of cards as a value of player_cards dict
        """
        return self.player_cards[player]

    def __end_game(self, card_list, player):
        if not list(card_list):
            self.__notify_events("on_game_ended", player)
            return


    def __remove_cards(self, cards_list, card_list):
        """Remove all elements of a card list from cards_list

        Arguments:
            cards: origin cards list
            card_list: list of cards that you need to get rid of
        """
        for card in card_list:
            cards_list.remove(card)

    def __compare_card_list(self,card_list2, card_list1):
        """Compare list of TienLencards

        Arguments:
            card_list2: (list) list of TienLenCard
            card_list1: (list) list of TienLenCard

        Returns:
            True if card_list2 > card_list1
            False otherwise
        """
        return (len(card_list2) == len(card_list1) and card_list1[-1] > card_list2[-1])


    def __deal_cards_the_first_time(self):
        total_cards_session = TienLenCard.generate_deck(shuffle=True)
        for i in range(len(self.players)):
            self.player_cards.setdefault(self.players[i], [total_cards_session.pop() for j in range(13)])
            self.player_cards[self.players[i]] = sorted(self.player_cards[self.players[i]])

    def run(self):
        """ Run game"""

        # Initialize a temp list to store player in one game session
        self.__process_new_session()
        is_end_game = True
        is_game_started = False
        is_cards_dealt = False

        while is_end_game:

            if len(self.players) == 1:
                raise OnlyOnePlayerJoin("Please wait one more player")
            self.__notify_events("on_game_started")
            is_game_started = True

            self.__deal_cards_the_first_time()
            self.__notify_events("on_cards_dealt", self.__get_card_of_each_player)
            is_cards_dealt = True

            # EVENT run_game_round
            is_round_started = False
            winner_in_round = ''
            current_round = 0

            # ROUND STARTED
            while True:
                self.__process_new_round()
                is_the_first_player = True
                # EVENT ON ROUND STATED
                self.__notify_events("on_round_started")
                is_round_started = True
                current_round += 1
                logging.info("CURRENT ROUND is %s", current_round)

                # EVENT ON PLAYER IN TURN
                if current_round == 1: # round 1
                    # Identify the first player who hold min card
                    player_hold_min_card = min(self.player_cards.items(), key=lambda val : val[1])
                    fist_player = player_hold_min_card[0]
                else: # round2 -->
                    # Identify the first player as the winner of the previous round
                    fist_player = winner_in_round

                # Get index of the player to start round
                index_to_start = list(self.player_cards.keys()).index(fist_player)

                current_player_cards = [] # temp list to store cards
                i = index_to_start
                is_end_turn = True

                # Define end turn
                while is_end_turn:
                    player_count = len(self.players_in_round)

                    # Get index of current player
                    current_player_index = (i % player_count)

                    # Get current player
                    player = self.players_in_round[current_player_index][0]

                    # Notify all players
                    self.__notify_events("on_player_in_turn", player)

                    # Update the list of cards of each player
                    the_rest_cards = self.__get_card_of_each_player(player)

                    # Skip the player who won previous round
                    if self.players_in_round[current_player_index][1] is False:
                        i += 1
                        continue

                    # Skip the player who win game
                    if not list(the_rest_cards):
                        i += 1
                        continue
                    tienlentrick_object_input = player.play(self)

                    # Get a list of player's cards input
                    if tienlentrick_object_input is not None:
                        prev_player_cards = tienlentrick_object_input[0].cards

                    # THE FIEST PLAYER
                    if is_the_first_player is True:
                        if current_round == 1: # round 1
                            if min(prev_player_cards) == min(the_rest_cards):
                                current_player_cards.extend(prev_player_cards)
                                self.__remove_cards(the_rest_cards, prev_player_cards)
                                # check if end game
                                self.__end_game(the_rest_cards, player)
                                i += 1
                                is_the_first_player = False
                                continue
                            else:
                                logging.info("YOU MUST PLAY THE SMALLEST CARD")
                                continue

                        else: # round2 -->
                            current_player_cards.extend(prev_player_cards)
                            self.__remove_cards(the_rest_cards, prev_player_cards)
                            self.__end_game(the_rest_cards, player)
                            i += 1
                            is_the_first_player = False
                            continue

                   # FROM THE 2ND PLAYER
                   # if the player has still not passed his turn
                    if self.players_in_round[current_player_index][1]:
                        # In case player skips his turn
                        if tienlentrick_object_input is None:
                            self.players_in_round[current_player_index][1] = False
                            if len([p[1]for p in self.players_in_round if p[1] is False])\
                                != len(self.players_in_round) - 1:
                                i += 1
                                continue

                            else:
                                winner_in_round = [p[0] for p in self.players_in_round if p[1] is True][0]
                                self.__notify_events("on_round_ended",winner_in_round)
                                break

                        # Compare cards
                        if self.__compare_card_list(current_player_cards, prev_player_cards):
                            current_player_cards = prev_player_cards
                            i += 1
                        else:
                            logging.info("Your cards are not suitable cards.")
                            continue
                        self.__remove_cards(the_rest_cards, prev_player_cards)
                        self.__end_game(the_rest_cards, player)


def main():
    """Run"""

    game_session1 = GameSession("Tiến Lên Table 1")
    pc1 = PC('PLAYER 0')
    pc2 = PC('PLAYER 1')
    pc3 = PC('PLAYER 2')
    pc4 = PC('PLAYER 3')
    pc1.join_game_session(game_session1)
    pc2.join_game_session(game_session1)
    pc3.join_game_session(game_session1)
    pc4.join_game_session(game_session1)
    game_session1.run()

if __name__ == "__main__":
    main()