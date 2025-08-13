"""
Dealer Management for Blackjack Game

This module implements the Dealer class which extends the base Hand class
with blackjack-specific dealer functionality including hole card management,
standard dealer rules, and comprehensive status display.

Classes:
    Dealer: Extends Hand with dealer-specific blackjack mechanics

Features:
- Hole card management with reveal functionality
- Standard blackjack dealer rules (hit on 16, stand on 17)
- Soft 17 handling (dealer hits on Ace+6)
- Blackjack detection and bust checking
- Professional display with hidden/revealed card states
- Comprehensive status reporting

Author: Artiom Lisin
"""

from typing import List

from blackjack_deck import Card
from hand import Hand


class Dealer(Hand):
    """
    Dealer class for blackjack gameplay with standard casino rules.
    
    This class represents the casino dealer with all standard blackjack rules
    including hole card management, hitting/standing decisions, and blackjack
    detection. The dealer follows strict casino rules for gameplay decisions.
    
    Attributes:
        hole_card_hidden (bool): Whether the first card is face-down
        has_revealed (bool): Whether the hole card has been revealed this round
        
    Dealer Rules Implemented:
    - Dealer hits on 16 or less
    - Dealer hits on soft 17 (Ace + 6)
    - Dealer stands on hard 17 or higher
    - Hole card starts hidden, revealed after player actions
    - Automatic blackjack detection and handling
        
    Note:
        Dealer inherits all hand management from the Hand class,
        including card value calculation and ace handling.
    """

    def __init__(self, initial_cards: List[Card]):
        """
        Initialize dealer with initial cards and hidden hole card.
        
        Args:
            initial_cards (List[Card]): Initial 2-card dealer hand
            
        Note:
            Dealer starts with hole card hidden (first card face-down).
            Blackjack detection is deferred until cards have blackjack values assigned.
            The has_revealed flag tracks whether hole card was shown this round.
        """
        super().__init__(initial_cards)
        self.hole_card_hidden = True  # First card starts face-down
        self.has_revealed = False     # Track if hole card was revealed this round

    def _check_for_blackjack(self) -> bool:
        """
        Internal method to check if dealer has blackjack (21 with 2 cards).
        
        Validates that the dealer has exactly 2 cards with properly assigned
        blackjack values, then checks if any hand value equals 21.
        
        Returns:
            bool: True if dealer has blackjack, False otherwise
            
        Note:
            This is an internal method used by the has_blackjack property.
            Ensures cards have blackjack_value assigned before checking.
        """
        if len(self.current_hand) == 2:
            # Ensure all cards have blackjack values assigned
            if all(card.blackjack_value is not None for card in self.current_hand):
                hand_values = self.get_hand_value()
                return 21 in hand_values
        return False

    @property
    def has_blackjack(self) -> bool:
        """
        Property to check for dealer blackjack when accessed.
        
        Returns:
            bool: True if dealer has blackjack (21 with exactly 2 cards)
            
        Note:
            This is a property that calls _check_for_blackjack() internally.
            Can be accessed like an attribute: dealer.has_blackjack
        """
        return self._check_for_blackjack()

    def reveal_hole_card(self) -> None:
        """
        Reveal the dealer's hole card (first card) and show results.
        
        Changes the hole card from hidden to visible, displays the revealed card
        to players, checks for dealer blackjack, and shows the complete hand.
        This typically happens after all players have completed their turns.
        
        Output:
        - Announces the revealed hole card
        - Declares dealer blackjack if applicable
        - Shows complete dealer hand with totals
        
        Note:
            Can only reveal once per round. Sets has_revealed flag to True.
            If already revealed, this method has no effect.
        """
        if self.hole_card_hidden:
            self.hole_card_hidden = False
            self.has_revealed = True
            
            # Announce the revealed card
            hole_card = self.current_hand[0]
            print(f"\n🎯 Dealer reveals hole card: {hole_card.value} of {hole_card.suit}")
            
            # Check and announce blackjack
            if self.has_blackjack:
                print("🃏 DEALER HAS BLACKJACK!")
            
            # Show complete hand
            self.show_full_hand()

    def should_hit(self) -> bool:
        """
        Determine if dealer should hit based on standard blackjack rules.
        
        Implements standard casino dealer rules:
        - Hit on 16 or less
        - Hit on soft 17 (Ace counted as 11, total is 17)
        - Stand on hard 17 or higher
        - Never hit if busted or has blackjack
        
        Returns:
            bool: True if dealer should take another card, False if should stand
            
        Dealer Decision Logic:
        1. If busted or has blackjack → Don't hit
        2. If soft 17 (Ace+6) → Hit (house rule)
        3. If 16 or less → Hit
        4. If hard 17+ → Stand
        
        Note:
            Soft 17 rule: Dealer must hit when holding Ace+6 (or equivalent).
            This gives the house a slight advantage over "dealer stands on all 17s".
        """
        # Never hit if busted
        if self.is_bust():
            return False
            
        hand_values = self.get_hand_value()
        
        # Never hit if dealer has blackjack
        if self.has_blackjack:
            return False
        
        # Check for soft 17 (Ace counted as 11, total is 17)
        if 17 in hand_values and len(hand_values) > 1:
            # This is a soft 17 - dealer must hit per casino rules
            return True
        
        # Standard rule: hit on 16 or less, stand on 17 or more
        return max(hand_values) < 17

    def show_hand(self, hide_hole_card: bool = True) -> None:
        """
        Display the dealer's hand with optional hole card hiding.
        
        Args:
            hide_hole_card (bool, optional): Whether to hide the first card. 
                                           Defaults to True.
                                           
        Note:
            This is the main method for displaying dealer hands.
            Automatically chooses between hidden and full display modes
            based on the hide_hole_card parameter and current game state.
        """
        if hide_hole_card and self.hole_card_hidden:
            self._show_hand_with_hidden_card()
        else:
            self.show_full_hand()

    def _show_hand_with_hidden_card(self) -> None:
        """
        Internal method to show dealer's hand with the first card hidden.
        
        Displays the dealer's hand with the hole card face-down, showing only
        visible cards and their potential values. Provides strategic information
        about what the hidden card could add to the total.
        
        Display Elements:
        - Hidden card shown as [Hidden Card] with card back emoji
        - Visible cards with full suit information
        - Calculated total of visible cards
        - Range indication for possible total with hidden card
        
        Note:
            This is an internal method called by show_hand() when appropriate.
            Only shows information that players would have access to in real blackjack.
        """
        if len(self.current_hand) < 2:
            return
            
        # Separate visible cards from hidden hole card
        visible_cards = self.current_hand[1:]  # All cards except first
        card_display = ["🂠 [Hidden Card]"] + [
            f"{card.value} of {card.suit}" for card in visible_cards
        ]
        
        print(f"🎰 Dealer's hand: {' | '.join(card_display)}")
        
        # Calculate and display visible card values
        if visible_cards:
            visible_total = 0
            visible_aces = 0
            
            # Sum visible cards with ace handling
            for card in visible_cards:
                value = card.blackjack_value
                if isinstance(value, list):
                    # This is an ace - use low value and count it
                    visible_total += value[0]  # Low value (1)
                    visible_aces += 1
                else:
                    # Regular card - add its value
                    visible_total += value if value is not None else 0
            
            # Display visible totals with ace flexibility
            if visible_aces > 0:
                high_total = visible_total + (10 * visible_aces)
                print(f"   🔍 Showing: {visible_total}/{high_total} (+ hidden card)")
            else:
                print(f"   🔍 Showing: {visible_total} (+ hidden card)")
        
        # Hint about hidden card possibilities
        print(f"   ❓ Hidden card could be worth 1-11 points")

    def show_full_hand(self) -> None:
        """
        Show dealer's complete hand with all cards revealed and total values.
        
        Displays the complete dealer hand with all cards visible, calculated
        totals, and current game status. Used when hole card is revealed or
        for final hand evaluation.
        
        Display Elements:
        - All cards with suit information
        - Complete hand total(s) with ace handling
        - Game status (Blackjack, Bust, Standing value)
        - Dealer decision indicator (stand/hit)
        
        Status Indicators:
        - 🃏 BLACKJACK: Exactly 21 with 2 cards
        - 💥 BUST: All possible totals exceed 21
        - 🛑 Standing: Dealer stops hitting at this value
        
        Note:
            This method shows complete information available after hole card reveal.
            For hands with aces, displays both possible totals (soft/hard).
        """
        # Display all cards
        card_display = [f"{card.value} of {card.suit}" for card in self.current_hand]
        print(f"🎰 Dealer's hand: {' | '.join(card_display)}")
        
        # Display hand totals
        hand_values = self.get_hand_value()
        if len(hand_values) == 1:
            print(f"   Dealer's total: {hand_values[0]}")
        else:
            # Show both values for hands with aces
            print(f"   Dealer's totals: {min(hand_values)}/{max(hand_values)}")
        
        # Display current status
        if self.has_blackjack:
            print("   🃏 BLACKJACK!")
        elif self.is_bust():
            print("   💥 BUST!")
        elif not self.hole_card_hidden and not self.should_hit():
            best_value = self.get_best_hand_value()
            print(f"   🛑 Dealer stands with {best_value}")

    def is_bust(self) -> bool:
        """
        Check if dealer is bust (all possible hand values exceed 21).
        
        Returns:
            bool: True if all hand values are over 21, False otherwise
            
        Note:
            Unlike players, dealer continues hitting until bust or stands.
            Bust means dealer loses to all non-busted players automatically.
        """
        hand_values = self.get_hand_value()
        return all(value > 21 for value in hand_values)

    def get_best_hand_value(self) -> int:
        """
        Get the best possible hand value (closest to 21 without going over).
        
        Selects the optimal hand value from all possible values, preferring
        the highest value that doesn't exceed 21. If all values bust,
        returns the lowest value.
        
        Returns:
            int: Best possible hand value for the dealer
            
        Selection Logic:
        1. If any values are ≤21, return the highest valid value
        2. If all values are >21 (bust), return the lowest value
        
        Example:
            - Hand values [7, 17]: Returns 17 (best non-bust)
            - Hand values [22, 32]: Returns 22 (lowest bust value)
            
        Note:
            This is used for final hand evaluation and comparison with players.
        """
        hand_values = self.get_hand_value()
        valid_values = [value for value in hand_values if value <= 21]
        
        if valid_values:
            # Return highest valid value (closest to 21 without busting)
            return max(valid_values)
        else:
            # All values are over 21 (bust), return the smallest bust value
            return min(hand_values)

    def get_status_summary(self) -> str:
        """
        Get a concise status summary for display purposes.
        
        Returns:
            str: Brief status description for UI display
            
        Possible Returns:
        - "BLACKJACK": Dealer has 21 with 2 cards
        - "BUST": Dealer's hand exceeds 21
        - "Hidden card": Hole card not yet revealed
        - "Total: X": Dealer's final hand value
        
        Note:
            This method provides quick status information for game UI.
            Used in scoreboard displays and game state summaries.
        """
        if self.has_blackjack:
            return "BLACKJACK"
        elif self.is_bust():
            return "BUST"
        elif self.hole_card_hidden:
            return "Hidden card"
        else:
            best_value = self.get_best_hand_value()
            return f"Total: {best_value}"
