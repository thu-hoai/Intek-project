#!/usr/bin/env python3
"""Build a core of Tien Len Trick"""
import time
import random
import enum
import pprint
import itertools
from tienlencard import TienLenCard
from card import Card
from constants import *


# Waypoint 9: Card Combinations
class TienLenTrick:
    """Class define a legal play by valid combination of cards"""
    TrickType = enum.Enum(
        'TrickType', 'single pair triple four_of_a_kind sequence double_sequence')

    def __init__(self, trick_type, cards):

        if self.__class__.__name__ == TienLenTrick.__name__:
            raise Exception(
                f"The Class {self.__class__.__name__}\
                must be instantiated with its factory methods")

        self.trick_type = trick_type
        self.cards = cards

    @staticmethod
    def __build_TienLenTrick(trick_type, cards):
        class __TienLenTrickImpl(TienLenTrick):
            pass

        return __TienLenTrickImpl(trick_type, cards)

    @staticmethod
    def __check_card(objects):
        """Check and return a list of TienLenCard object

        Args: objects: a list of objects

        Raises:
            ValueError: exist the object which is not a TienLenCard object
            ValueError: exist the the same objects

        Returns: a list of TienLenCard object
        """
        # Check empty cards list or not
        if not list(objects):
            raise ValueError("Invalid argument cards")

        for card in objects:
            # Raise error if the list contains the different object with Tienlen
            if not isinstance(card, TienLenCard):
                raise ValueError("The list cards contain TienLenCard objects only")
            # Raise error if the list contains the same cards
            if objects.count(card) > 1:
                raise ValueError("Must not contain the same TienLencards")

        return objects

    def __str__(self):
        return f'{self.trick_type}, {self.cards}'

    def __repr__(self):
        return f'{self.__class__.__name__}.{self.trick_type}, {self.cards}'

    # Waypoint 10: Validate Card Combinations
    @staticmethod
    def is_single(cards):
        """Check if a single card

        Args: cards objects: a list of objects

        Returns:
            True if this list of cards corresponds to the type of combination
                that this function checks
            False otherwise.
        """
        # Check if given cards list is valid or not
        TienLenTrick.__check_card(cards)

        return len(cards) == 1

    @staticmethod
    def is_pair(cards):
        """Check if the type combination is Two cards of the same rank

        Args: cards objects: a list of objects

        Returns:
            True if this list of cards corresponds to the type of combination
                that this function checks
            False otherwise.
        """
        # Check if given cards list is valid or not
        TienLenTrick.__check_card(cards)

        # Not a pair if the number of cards != 2
        if len(cards) != 2:
            return False
        # Compare if the same rank
        if cards[0].rank != cards[1].rank:
            return False

        return True

    @staticmethod
    def is_triple(cards):
        """Check if the type combination is Three cards of the same rank

        Args: cards objects: a list of objects

        Returns:
            True if this list of cards corresponds to the type of combination
                that this function checks
            False otherwise.
        """
        # Check if given cards list is valid or not
        TienLenTrick.__check_card(cards)

        # Not a triple if the number of cards != 3
        if len(cards) != 3:
            return False

        # Not a triple if exist a different card
        return len({cards[i].rank for i in range(3)}) == 1

    @staticmethod
    def is_four_of_a_kind(cards):
        """Check if the type combination is Four cards of the same rank.

        Args: cards objects: a list of objects

        Returns:
            True if this list of cards corresponds to the type of combination
                that this function checks
            False otherwise.
        """
        # Check if given cards list is valid or not
        TienLenTrick.__check_card(cards)

        # Not a four type if the number of cards != 4
        if len(cards) != 4:
            return False

        # Not a four type if exist a different card
        return len({cards[i].rank for i in range(4)}) == 1

    @staticmethod
    def is_sequence(cards):
        """Check if the type combination is Three or more cards of consecutive rank.

        Args: cards objects: a list of objects

        Returns:
            True if this list of cards corresponds to the type of combination
                that this function checks
            False otherwise.
        """
        # Check if given cards list is valid or not
        TienLenTrick.__check_card(cards)

        # Not a sequense type if the number is lower than 3 or greater than 13
        if len(cards) < 3 or len(cards) > 13:
            return False

        # Create a sorted list of given ranks
        rank_sequence = sorted([TIENLEN_RANKS[card.rank] for card in cards if card.rank != "2"])

        # Check if above rank list is the cards of consecutive rank or not
        for j in range(len(rank_sequence) - 1):
            if rank_sequence[j + 1] - rank_sequence[j] != 1:
                return False
        return True

    @staticmethod
    def is_double_sequence(cards):
        """Check if the type combination is Three or more pairs of consecutive rank.

        Args: cards objects: a list of objects

        Returns:
            True if this list of cards corresponds to the type of combination
                that this function checks
            False otherwise.
        """
        # Check if given cards list is valid or not
        TienLenTrick.__check_card(cards)

        # Not a double sequense if the number is lower than 6 or greater than 12
        if len(cards) < 6 or len(cards) > 12:
            return False

        # Create a sorted list of given ranks
        rank_sequence = sorted([TIENLEN_RANKS[card.rank] for card in cards if card.rank != "2"])

        # Check if above rank list is a pair card list or not
        if len(set(rank_sequence)) != len(rank_sequence) // 2:
            return False

        # Check if above rank list is pairs of consecutive rank or not
        for j in range(len(rank_sequence) - 2):
            if rank_sequence[j + 2] - rank_sequence[j] != 1:
                return False
        return True

    # Waypoint 11: Find Singles
    @classmethod
    def find_singles(cls, cards):
        """Return a list of objects of all the single cards

        Args: cards a list of objects card

        Returns: a list of objects of all the single cards
        """
        # Check if given cards list is valid or not
        cls.__check_card(cards)

        # Return a list of objects of all the single cards
        return [cls.__build_TienLenTrick(cls.TrickType.single, [card]) for card in cards]

    # Waypoint 12: Find Pairs
    @classmethod
    def find_pairs(cls, cards):
        """ Get a list of all the pairs of objects TienLenTrick from given lists

        Args: cards: (list) a list of objects TienLenCard

        Returns: a list of all the pairs (list of objects TienLenTrick)
        """
        # Get the type of the trick as pair
        trick_type = TienLenTrick.TrickType.pair

        # Return a list of all the pairs
        return cls.__support_find_pairs_triple_four_card(cards, trick_type)

    # Waypoint 13: Find Triples
    @classmethod
    def find_triples(cls, cards):
        """ Get a list of all the triples of objects TienLenTrick from given lists

        Args: cards: (list) a list of objects TienLenCard

        Returns: a list of all the triples (list of objects TienLenTrick)
        """
        # Get the type of the trick as triple
        trick_type = TienLenTrick.TrickType.triple

        # Return a list of all the triple
        return cls.__support_find_pairs_triple_four_card(cards, trick_type)

    @classmethod
    # Waypoint 14: Find Fours of a Kind
    def find_fours_of_a_kind(cls, cards):
        """ Get a list of all the fours of objects TienLenTrick from given lists

        Args: cards: (list) a list of objects TienLenCard

        Returns: a list of all the fours (list of objects TienLenTrick)
        """
        # Get the type of the trick as four_of_a_kind
        trick_type = TienLenTrick.TrickType.four_of_a_kind

        # Return a list of all the pairs
        return cls.__support_find_pairs_triple_four_card(cards, trick_type)

    @classmethod
    # Waypoint 15: Find Sequences
    def find_sequences(cls, cards):
        """ Get a nested list of all the combinations of cards that form a sequence.

        Arguments: cards: (list) a list of objects TienLenCard

        Returns: a nested list of all the combinations of cards that form a sequence.
        """

        # The type of the trick as sequence
        trick_type = TienLenTrick.TrickType.sequence

        return cls.__support_find_sequences_double_sequences(cards, trick_type)

    @classmethod
    # Waypoint 16: Find Double Sequences
    def find_double_sequences(cls, cards):
        """ Get a nested list of all the combinations of cards that form a double sequence.

        Arguments: cards: (list) a list of objects TienLenCard

        Returns: a nested list of all the combinations of cards that form a double sequence.
        """

        # The type of the trick as double_sequence
        trick_type = TienLenTrick.TrickType.double_sequence

        return cls.__support_find_sequences_double_sequences(cards, trick_type)

    @staticmethod
    def __combine_card(cards_list, group):
        """Combine cards from given list by given group and
            return nested list of cards

        Args:
            cards_list: (list) a list that is in need of separate
            group: (int) define the number of elements which is in need of grouping

        Returns: (list) nested lists of combination of given object by group
        """
        return [list(elem) for elem in itertools.combinations(cards_list, group)]

    @staticmethod
    def __group_card_by_rank(cards):
        """Group cards by their ranks and store them to a dictionary

        Args: cards: (list) a lisf of objects of TienLenCard

        Returns: A dictionary with (key, value) is (rank, a list TienLenCard obj)
        """
        # Check if given cards list is valid or not
        TienLenTrick.__check_card(cards)

        # Initialize a dict with (key, value) is (rank, a list TienLenCard obj)
        group_by_rank_dict = {}
        cards = TienLenCard.sort_cards(cards)
        for card in cards:
            group_by_rank_dict.setdefault(TIENLEN_RANKS[card.rank], []).append(card)

        return group_by_rank_dict

    @staticmethod
    def __check_type_group_card(cards, trick_type):
        """Check if given cards corresponds to the type of combination

        Arguments:
            cards: a list of objects
            trick_type : type of combination

        Returns:
            True if this list of cards corresponds to
                the type of combination that this function checks
            False otherwise.
        """

        type_card = trick_type.name
        if type_card == 'pair':
            return TienLenTrick.is_pair(cards)

        if type_card == 'triple':
            return TienLenTrick.is_triple(cards)

        if type_card == 'four_of_a_kind':
            return TienLenTrick.is_four_of_a_kind(cards)

        if type_card == 'sequence':
            return TienLenTrick.is_sequence(cards)

        if type_card == 'double_sequence':
            return TienLenTrick.is_double_sequence(cards)

    @classmethod
    def __support_find_pairs_triple_four_card(cls, cards, trick_type):
        """Return list of objects TienLenTrick correspond to given type of combination

        Arguments:
            cards: a list of objects
            trick_type: (enum 'TrickType') a type of a trick
            group_num: (int) type of combination

        Returns: a list of objects TienLenTrick correspond to given type of combination
        """
        # A dictionary with (key, value) is (rank, a list TienLenCard obj)
        groups_by_rank_dict = cls.__group_card_by_rank(cards)

        # Initialize a list of all the pairs/triple/four kind
        group_list = []

        # Get the number of cards correspond to trick type
        group_num = GROUP_BY_TYPE[trick_type.name]

        # Loop through each list of Tienlen cards which have their same rank
        for same_rank_cards_list in groups_by_rank_dict.values():
            # For each same_rank_cards_list, combine n same values to get
            # all combinations of each of same_rank_cards_list
            card_combine_lists = cls.__combine_card(same_rank_cards_list, group_num)
            # Check all combinations if their type combination is pairs type or not
            for card_list in card_combine_lists:
                # If ok, add them to a result list
                if cls.__check_type_group_card(card_list, trick_type):
                    group_list.append(cls.__build_TienLenTrick(trick_type, card_list))

        return group_list

    @staticmethod
    def __build_variable_length_sequence_ranks(dic):
        """ Return list of all the possible combinations of lists of values of dictionary
            bases on consecutive keys of given dictionary

        Args: dic (dict): a dictionary

        Return: all the possible combinations of lists of values of given dictionary
        """
        # initialize with the first value in the dict
        keys_list = [[list(dic.keys())[0]]]
        values_lists = [list(dic.values())[0]]
        for i, val in enumerate(list(dic.keys())[1:]):
            if val - keys_list[-1][-1] > 1:
                # create a new group
                keys_list.append([val])
                values_lists.extend([dic[val]])
            else:
                # append to the most recent group
                keys_list[-1].append(val)
                values_lists[-1].extend(dic[val])

        return values_lists

    @classmethod
    # Waypoint 15: Find Sequences
    def __support_find_sequences_double_sequences(cls, cards, trick_type):
        """ Get a nested list of all the combinations of cards that form a sequence
            or double_sequence

        Arguments: cards: (list) a list of objects TienLenCard

        Returns: a nested list of all the combinations of cards that form a sequence
            or double_sequence
        """

        # A dictionary with (key, value) is (rank, a list TienLenCard obj)
        groups_by_rank_dict = cls.__group_card_by_rank(cards)

        # Initialize a list of all sequence
        group_lst = []

        # A list of all the possible combinations of Tienlen cards
        # bases on consecutive ranks
        group_by_index = cls.__build_variable_length_sequence_ranks(groups_by_rank_dict)

        # Get the number of cards correspond to trick type
        group_num = GROUP_BY_TYPE[trick_type.name]

        # Loop to get a nested list of all the combinations of cards that form a sequence.
        for ele_list in group_by_index:

            # Skip if list of the number of cards in list < 3(sequences) or < 6(double_sequence)
            if len(ele_list) < group_num[0]:
                continue

            # Combine each of a list from 3 to its len
            for i in range(group_num[0], len(ele_list) + 1, group_num[1]):
                combination_nested_list = cls.__combine_card(ele_list, i)
                for combination_list in combination_nested_list:
                    # Get lists that satisfy as a sequence
                    if cls.__check_type_group_card(combination_list, trick_type):
                        group_lst.append(cls.__build_TienLenTrick(trick_type, combination_list))

        return group_lst

    # Waypoint 19: Build a Tiến Lên Trick from a List of Cards
    @classmethod
    def build_trick(cls, cards):
        """ All possible combination of cards corresponds to a valid Tiến Lên trick

        Arguments: cards: a list of objects

        Raises: ValueError: no combination trick is found

        Returns: a list of all possible combination of cards corresponds
            to a valid Tiến Lên trick
        """

        # A list to check a valid trick
        is_valid_trick = [cls.is_single(cards), cls.is_pair(cards), cls.is_triple(cards),
                          cls.is_four_of_a_kind(cards), cls.is_sequence(cards),
                          cls.is_double_sequence(cards)]
        # A list to return a cards list corresponds to above valid trick list
        valid_trick_list = [cls.find_singles(cards), cls.find_pairs(cards), cls.find_triples(cards),
                            cls.find_fours_of_a_kind(cards), cls.find_sequences(cards),
                            cls.find_double_sequences(cards)]

        # Loop in is_valid_trick to find a valid trick in given cards
        for index, valid_trick in enumerate(is_valid_trick):
            if valid_trick:
                # Return cards corresponds to a valid trick
                return valid_trick_list[index]

        # Raise error if no valid combination found
        if not list(valid_trick_list[index]):
            raise ValueError(f"the cards don't correspond to a Tiến Len trick")


def main():
    """
    Demonstrate and run
    """
    # cards = [TienLenCard('4s'), TienLenCard('4h'), TienLenCard('5c'),
    # TienLenCard('6s'), TienLenCard('7c'), TienLenCard('7d'),
    # TienLenCard('Tc'), TienLenCard('Td'), TienLenCard('Jd'),
    # TienLenCard('Qc'), TienLenCard('Qd'), TienLenCard('As'),
    # TienLenCard('2d')]
    # tricks = TienLenTrick.find_sequences(cards)
    # pprint.pprint(tricks)

    # cards = [TienLenCard('Qh'), TienLenCard('4c'), TienLenCard('Qc'),
    #          TienLenCard('9s'), TienLenCard('5s'), TienLenCard('8d'),
    #          TienLenCard('Th'), TienLenCard('Qs'), TienLenCard('Ts'),
    #          TienLenCard('Kd'), TienLenCard('Jd'), TienLenCard('Js'),
    #          TienLenCard('Kh')]
    # tricks = TienLenTrick.find_pairs(cards)
    # pprint.pprint(tricks)

    # TEST FOR WAYPOINT 18
    # pprint.pprint(TienLenTrick.build_trick([TienLenCard('4d')]))
    pprint.pprint(TienLenTrick.build_trick([TienLenCard('4c'),
                                            TienLenCard('5h'), TienLenCard('6c')]))


if __name__ == "__main__":
    main()
