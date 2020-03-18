#!/usr/bin/env python3
import random
import enum
import pprint
import collections
from constants import *

class Card:
    """Class represent a card from a 52-card deck French playing cards."""

    def __init__(self, *card):
        """ The constructor for Card class

        Parameters:
            rank (An ASCII character): either a digit (2-9) or
                an uppercase letter (T, J, Q, K, A)
            suit: An ASCII lowercase letter (h , d , c , s) or
                Unicode character (♥ , ♦ , ♣ , ♠)
        """
        rank = None
        suit = None
        # In case arguments are not string type
        if not isinstance(card[0], str):
            raise ValueError("Not a string")

        # In case the number of args or len symbol is larger than 2
        if len(card[0]) not in (1, 2) or len(card) not in (1, 2):
            raise ValueError("Not a correct format")

        # Card is a tupple 2 elements
        if len(card) == 2:
            rank = card[0]
            suit = card[1]

        # Card is a symbol 1 element
        if len(card) == 1:
            rank = card[0][0]
            suit = card[0][1]

        # Validate rank and suit of a card
        if rank and rank not in RANKS:
            raise ValueError(f'Wrong rank {rank}')
        if suit and suit not in SUITS.values() and suit not in SUITS:
            raise ValueError(f'Wrong suit {suit}')

        self.__rank = rank
        self.__suit = suit
        self.__symbol = f'{rank}{suit}'

    @property
    def rank(self):
        """Rank of a card"""
        return self.__rank

    @property
    def suit(self):
        """Suit of a card"""
        return self.__suit

    @property
    def symbol(self):
        """Symbol of a card"""
        return self.__symbol

    # Waypoint 2: Human-Readable String Representation of a Card
    def __str__(self):
        """ Return a nicely string representation of a card object"""
        return self.__symbol

    # Waypoint 3: Official String Representation of a Card
    def __repr__(self):
        """ Return the official string representation of a card object"""
        return f"{self.__class__.__name__}('{self.__symbol}')"

    # Waypoint 7: Generate a 52-Card Deck French Playing Cards
    @classmethod
    def generate_deck(cls, shuffle=False):
        """ Return a list of playing cards which is shuffled or not

        Keyword Arguments:
            shuffle: whether the cards need to be shuffled (default: {False})
                True if the cards need to be shuffled

        Returns: a list of 52 French playing cards
        """
        # Initialize a list to store playings cards
        cards_list = [cls(rank, suit) for rank in RANKS for suit in SUITS]

        # In case shuffle is True, shuffle playing cards list
        if shuffle:
            random.shuffle(cards_list)
        return cards_list