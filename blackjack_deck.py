"""
Blackjack-Specific Deck Implementation

This module extends the generic Deck class to provide blackjack-specific
functionality, including proper card value assignment, multiple deck mixing,
and casino-style deck cutting.

Classes:
    BlackjackDeck: A specialized deck for blackjack games with multiple deck support

Features:
- Multi-deck support (default 6 decks, configurable)
- Automatic blackjack value assignment for all cards
- Casino-style deck cutting to remove predictability
- Proper card value handling for blackjack rules

Author: Artiom Lisin
"""

import random
from typing import List

from deck import Card, Deck


class BlackjackDeck(Deck):
    """
    Deck tailored for blackjack play.
    
    This class extends the generic Deck to provide blackjack-specific features
    including multiple deck mixing, automatic value assignment, and casino-style
    deck cutting practices.
    
    Class Attributes:
        deck_cut_range (tuple): Range for random deck cutting (60-75 cards from bottom)
        
    Instance Attributes:
        Inherits all attributes from Deck class
        
    Note:
        In blackjack, casinos typically use 6-8 decks shuffled together and cut
        to prevent card counting. This implementation follows those practices.
    """
    
    # Range for cutting deck - removes 60-75 cards from the bottom
    # This simulates casino practice of using a cut card
    deck_cut_range = (60, 75)

    def __init__(self, num_decks: int = 6) -> None:
        """
        Initialize a blackjack deck with multiple standard decks.
        
        Creates a shoe of multiple decks (standard casino practice), shuffles them,
        and cuts the deck by removing a random number of cards from the bottom.
        
        Args:
            num_decks (int): Number of standard 52-card decks to combine (default: 6)
            
        Note:
            - Standard casino blackjack uses 6-8 decks
            - Cards are cut from bottom to simulate casino cut card practice
            - All cards are automatically assigned blackjack values when drawn
        """
        # Initialize with a single deck first
        super().__init__()
        
        # Replicate the deck num_decks times for multi-deck play
        single_deck = list(self.deck)  # Create a copy of the original 52 cards
        self.deck = [
            Card(card.suit, card.value) 
            for _ in range(num_decks) 
            for card in single_deck
        ]
        
        # Shuffle the combined multi-deck shoe
        self.shuffle_deck()

        # Cut the deck (casino practice) - remove random number of cards from bottom
        cutval = random.randint(*self.deck_cut_range)
        bottom_cards = self.deck[-cutval:]  # Take cards from bottom
        self.discard_pile.extend(bottom_cards)  # Move them to discard
        self.deck = self.deck[:-cutval]  # Remove them from deck

    def draw_card(self, num_cards: int = 1) -> List[Card]:
        """
        Draw cards and assign blackjack values automatically.
        
        Extends the parent draw_card method to automatically assign proper
        blackjack values to each card as it's drawn. This ensures all cards
        have the correct game values when used in gameplay.
        
        Args:
            num_cards (int): Number of cards to draw (default: 1)
            
        Returns:
            List[Card]: List of drawn cards with blackjack_value assigned
            
        Raises:
            ValueError: If the deck is empty and cards cannot be drawn
            
        Note:
            Card values are assigned as follows:
            - Number cards (2-10): Face value
            - Face cards (J, Q, K): 10
            - Aces: [1, 11] (flexible value)
        """
        # Draw cards using parent method
        cards = super().draw_card(num_cards)
        
        # Assign blackjack values to each drawn card
        for card in cards:
            card.blackjack_value = self.blackjack_value(card)
        
        return cards

    @staticmethod
    def blackjack_value(card: Card):
        """
        Calculate the blackjack value for a given card.
        
        Assigns the appropriate blackjack value based on card face value
        according to standard blackjack rules.
        
        Args:
            card (Card): The card to evaluate
            
        Returns:
            int or List[int]: The blackjack value(s) for the card
            
        Raises:
            ValueError: If the card has an invalid/unrecognized value
            
        Value Rules:
            - Number cards (2-10): Face value as integer
            - Face cards (Jack, Queen, King): 10
            - Ace: [1, 11] (player can choose optimal value)
        """
        # Number cards: use face value
        if card.value in ["2", "3", "4", "5", "6", "7", "8", "9", "10"]:
            return int(card.value)
        
        # Face cards: all worth 10
        if card.value in ["Jack", "Queen", "King"]:
            return 10
        
        # Ace: can be 1 or 11 (flexible value)
        if card.value == "Ace":
            return [1, 11]
        
        # Invalid card value
        raise ValueError(f"Invalid card value: {card.value}")
