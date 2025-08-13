"""
Generic Playing Card Deck Implementation

This module provides the foundation for playing card games with a standard
52-card deck. It includes the Card dataclass and a generic Deck class that
can be extended for specific games like Blackjack.

Classes:
    Card: Represents a single playing card with suit, value, and optional game-specific value
    Deck: Generic deck of 52 playing cards with shuffle, draw, and discard functionality

The design allows for extension to game-specific decks (like BlackjackDeck) while
maintaining a clean separation of concerns.

Author: Artiom Lisin
"""

from dataclasses import dataclass
from random import shuffle
from typing import List, Union, Final


@dataclass
class Card:
    """
    Representation of a single playing card.
    
    This dataclass encapsulates all the properties of a playing card,
    including suit, face value, and an optional game-specific value
    (like blackjack_value for blackjack games).
    
    Attributes:
        suit (str): The suit of the card (Hearts, Diamonds, Clubs, Spades)
        value (str): The face value (2-10, Jack, Queen, King, Ace)
        blackjack_value (Union[int, List[int], None]): Game-specific value
            - For numbered cards: int (2-10)
            - For face cards: int (10)
            - For Aces: List[int] ([1, 11])
            - For uninitialized cards: None
    """
    suit: str
    value: str
    blackjack_value: Union[int, List[int], None] = None


class Deck:
    """
    Generic deck of playing cards.
    
    This class provides a standard 52-card deck with basic operations
    like shuffling, drawing cards, and managing a discard pile. It serves
    as the base class for game-specific deck implementations.
    
    Class Attributes:
        SUITS: Immutable list of the four standard card suits
        VALUES: Immutable list of the thirteen card values in order
    
    Instance Attributes:
        deck: List of cards currently in the deck
        discard_pile: List of cards that have been discarded
    """

    # Class constants for standard deck composition
    SUITS: Final = ["Hearts", "Diamonds", "Clubs", "Spades"]
    
    VALUES: Final = [
        "2", "3", "4", "5", "6", "7", "8", "9", "10",
        "Jack", "Queen", "King", "Ace",
    ]

    def __init__(self) -> None:
        """
        Initialize a standard 52-card deck.
        
        Creates all combinations of suits and values, initializes an empty
        discard pile, and shuffles the deck for immediate use.
        """
        # Create all 52 cards (4 suits × 13 values)
        self.deck: List[Card] = [
            Card(suit, value) for suit in self.SUITS for value in self.VALUES
        ]
        self.discard_pile: List[Card] = []
        self.shuffle_deck()

    def draw_card(self, num_cards: int = 1) -> List[Card]:
        """
        Draw one or more cards from the top of the deck.
        
        Args:
            num_cards (int): Number of cards to draw (default: 1)
            
        Returns:
            List[Card]: List of drawn cards
            
        Raises:
            ValueError: If the deck is empty and cards cannot be drawn
            
        Note:
            Cards are removed from the deck when drawn. For game-specific
            behavior (like assigning blackjack values), override this method
            in subclasses.
        """
        if not self.deck:
            raise ValueError("No more cards in the deck.")
        
        # Take cards from the top (beginning) of the deck
        drawn = self.deck[:num_cards]
        self.deck = self.deck[num_cards:]
        return drawn

    def shuffle_deck(self) -> List[Card]:
        """
        Shuffle the deck in place and return it.
        
        Uses Python's random.shuffle() to randomize card order.
        This method modifies the deck in place for efficiency.
        
        Returns:
            List[Card]: The shuffled deck (same reference as self.deck)
        """
        shuffle(self.deck)
        return self.deck
    
    def discard_card(self, card_index: int) -> None:
        """
        Discard a card from the deck to the discard pile.
        
        This method moves a card from the main deck to the discard pile,
        which can be useful for certain game mechanics.
        
        Args:
            card_index (int): Index of the card to discard (0-based)
            
        Raises:
            IndexError: If card_index is out of range for the current deck
        """
        if card_index >= len(self.deck):
            raise IndexError("Card index out of range.")
        
        # Remove card from deck and add to discard pile
        discarded = self.deck.pop(card_index)
        self.discard_pile.append(discarded)

    def display_deck(self) -> None:
        """
        Display all cards currently in the deck.
        
        Prints each card with its position in the deck. Useful for
        debugging and game development purposes.
        """
        for i, card in enumerate(self.deck, 1):
            print(f"Card {i}: {card.value} of {card.suit}")

    def display_discard_pile(self) -> None:
        """
        Display all cards in the discard pile.
        
        Prints each discarded card with its position in the discard pile.
        Useful for tracking which cards have been played.
        """
        for i, card in enumerate(self.discard_pile, 1):
            print(f"Discarded Card {i}: {card.value} of {card.suit}")
