#!/usr/bin/env python3

# Define the list of rank of card
RANKS = ["3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A", "2"]

# Define a dictionary the suit of a card
SUITS = {
    "h": u"\u2665",  # Hearts
    "d": u"\u2666",  # Diamonds
    "c": u"\u2663",  # Clubs
    "s": u"\u2660",  # Spades
}
# Define for Tienlen Game
TIENLEN_RANKS = {"3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8,
                 "9": 9, "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14, "2": 15}
TIENLEN_SUITS = {"h": 4, "d": 3, "c": 2, "s": 1}

GROUP_BY_TYPE = {"pair": 2, "triple": 3, "four_of_a_kind": 4,
                "sequence": [3,1], "double_sequence": [6,2]}
