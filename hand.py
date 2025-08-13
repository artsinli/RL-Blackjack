"""
Hand Management for Card Games

This module provides the base Hand class that manages a collection of cards
and calculates hand values, with special handling for Aces in blackjack.
It serves as the foundation for both Player and Dealer classes.

Classes:
    Hand: Base class for managing a hand of cards with value calculation

Features:
- Automatic hand value calculation with ace flexibility
- Support for multiple possible hand values (soft/hard hands)
- Ace counting and value optimization
- Extensible design for game-specific hand rules

Author: Artiom Lisin
"""

from typing import List

from blackjack_deck import Card


class Hand:
    """
    Base hand class used for players and dealers.
    
    This class manages a collection of cards and provides value calculation
    with special handling for Aces, which can be worth 1 or 11 in blackjack.
    It automatically tracks all possible hand values and maintains an ace table
    for optimal value selection.
    
    Attributes:
        current_hand (List[Card]): List of cards currently in the hand
        hand_value (List[int]): All possible hand values (accounting for aces)
        ace_table (List[tuple[int, int]]): Mapping of ace count to hand values
        n_aces (int): Number of aces in the current hand
        
    Note:
        Hand values are automatically recalculated whenever cards are added.
        For hands with aces, multiple values represent soft/hard hand options.
    """

    def __init__(self, predraw: List[Card]):
        """
        Initialize a hand with an initial draw of cards.
        
        Args:
            predraw (List[Card]): Initial cards to add to the hand
            
        Raises:
            ValueError: If fewer than 2 cards are provided for initial draw
            
        Note:
            Most card games (especially blackjack) start with 2 cards,
            so this is enforced to ensure proper game initialization.
        """
        if len(predraw) < 2:
            raise ValueError("Must initiate a 2 card predraw to initialize a player")
        
        # Initialize hand state
        self.current_hand: List[Card] = list(predraw)  # Create copy to avoid mutation
        self.hand_value: List[int] = []
        self.ace_table: List[tuple[int, int]] = []
        self.n_aces = 0
        
        # Calculate initial hand value
        self.calc_hand_value()

    def add_card(self, card: Card) -> None:
        """
        Add a card to the hand and recalculate values.
        
        This method adds a new card to the hand and automatically recalculates
        all possible hand values, including ace optimizations.
        
        Args:
            card (Card): The card to add to the hand
            
        Note:
            Hand values are automatically updated after adding each card.
            This ensures the hand always reflects the current state.
        """
        self.current_hand.append(card)
        self.calc_hand_value()

    def get_hand_value(self) -> List[int]:
        """
        Get the current hand value(s).
        
        Recalculates and returns all possible hand values. For hands without aces,
        this returns a single value. For hands with aces, this returns multiple
        values representing different ways to count the aces.
        
        Returns:
            List[int]: All possible hand values
            
        Example:
            - Hand with 10, 5: [15]
            - Hand with Ace, 6: [7, 17] (ace as 1 or 11)
            - Hand with Ace, Ace, 9: [11, 21] (one ace as 1, other as 11)
        """
        self.calc_hand_value()
        return self.hand_value

    # Protected/Internal methods for hand calculation
    
    def calc_ace_table(self) -> None:
        """
        Calculate the ace value table for the current hand.
        
        Creates a mapping of different ace configurations to total hand values.
        This table helps determine optimal ace usage (as 1 or 11) for the hand.
        
        The ace table contains tuples of (aces_as_11, total_value) where:
        - aces_as_11: Number of aces counted as 11
        - total_value: Resulting hand total with that ace configuration
        
        Note:
            This is an internal method used by calc_hand_value().
            Only one ace can typically be counted as 11 without busting.
        """
        self.ace_table = [
            (i, self.hand_value[0] + 10 * i) 
            for i in range(self.n_aces + 1)
        ]

    def calc_hand_value(self) -> None:
        """
        Calculate all possible hand values considering ace flexibility.
        
        This method recalculates the hand value(s) from scratch, handling aces
        specially since they can be worth 1 or 11. The calculation process:
        
        1. Count aces and calculate base value (all aces as 1)
        2. If aces present, calculate alternate values (some aces as 11)
        3. Store all valid hand values for player decision making
        
        Hand Value Logic:
        - Non-ace cards: Use blackjack_value directly
        - Aces: Start as 1, then calculate alternatives with some as 11
        - Multiple values: Represent soft hands (ace counted as 11) vs hard hands
        
        Note:
            This method updates self.hand_value, self.n_aces, and self.ace_table.
            It's called automatically when cards are added or values are requested.
        """
        # Reset counters
        self.n_aces = 0
        low_total = 0
        
        # Calculate base value with all aces as 1
        for card in self.current_hand:
            value = card.blackjack_value
            
            if isinstance(value, list):
                # This is an ace - use low value (1) and count it
                low_total += value[0]  # value[0] is always 1 for aces
                self.n_aces += 1
            else:
                # Regular card - add its value (or 0 if None)
                low_total += value if value is not None else 0
        
        # Determine final hand values based on ace presence
        if self.n_aces:
            # Hand has aces - calculate soft and hard values
            # Soft hand: one ace as 11, others as 1 (if it doesn't bust)
            high_total = low_total + 10 * self.n_aces
            self.hand_value = [low_total, high_total]
            self.calc_ace_table()
        else:
            # No aces - single fixed value
            self.hand_value = [low_total]
