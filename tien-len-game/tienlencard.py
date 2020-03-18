#!/usr/bin/env python3
import random
import enum
import pprint
import collections
from card import Card
from constants import *
import itertools


class TienLenCard(Card):
    """Class TienLenCard represent a card Tienlen """

    def __init__(self, *args):
        super().__init__(*args)
        self.__tienlen_rank = TIENLEN_RANKS[self.rank]
        self.__tienlen_suit = TIENLEN_SUITS[self.suit]

    @property
    def tienlen_rank(self):
        """ Rank of Tienlen card"""
        return self.__tienlen_rank

    @property
    def tienlen_suit(self):
        """ Suit of Tienlen card"""
        return self.__tienlen_suit

    # Waypoint 6: Cards Comparison

    def __eq__(self, other):
        # Check class membership of TienlenCard
        # if not isinstance(other, __class__):
        #     raise TypeError("Not the same object")

        # In case equal ranks, return True if suit lower than, False otherwise
        return self.tienlen_rank == other.tienlen_rank and \
               self.tienlen_suit == other.tienlen_suit

    def __ge__(self, other):
        # Check class membership of TienlenCard
        if not isinstance(other, __class__):
            return NotImplemented

        return not self.__lt__(other)

    def __gt__(self, other):
        # Check class membership of TienlenCard
        if not isinstance(other, __class__):
            return NotImplemented

        # Return True if rank is greater than
        if self.tienlen_rank > other.tienlen_rank:
            return True
        # In case equal ranks, return True if suit lower than, False otherwise
        return self.tienlen_rank == other.tienlen_rank \
               and self.tienlen_suit > other.tienlen_suit

    def __lt__(self, other):
        # Check class membership of TienlenCard
        if not isinstance(other, __class__):
            return NotImplemented
        # Return True if rank is lower than
        if self.tienlen_rank < other.tienlen_rank:
            return True
        # In case equal ranks, return True if suit lower than, False otherwise
        return self.tienlen_rank == other.tienlen_rank and \
               self.tienlen_suit < other.tienlen_suit

    def __le__(self, other):
        # Check class membership of TienlenCard
        if not isinstance(other, __class__):
            return NotImplemented
        return not self.__gt__(other)

    @staticmethod
    def sort_cards(cards, reverse=False):
        """Sorting a list of cards

        Arguments:
            cards: a list of TienLenCard objects

        Keyword Arguments:
            reverse {bool} :identify if sorted in ascending or descending order
                (default: {False}: sorted in ascending order. True otherwise)

        Returns:
            the list of cards sorted in ascending order if the arg reverse is False,
            or in descending order if the argument reverse is True.
        """
        return sorted(cards, reverse=reverse)

