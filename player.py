"""
Player Management for Blackjack Game

This module implements the Player class which extends the base Hand class
with blackjack-specific functionality including betting, bankroll management,
and enhanced status displays with emojis and formatted output.

Classes:
    Player: Extends Hand with betting mechanics and game status display

Features:
- Comprehensive betting system with bet validation
- Bankroll management with bankruptcy detection
- Enhanced status display with emojis and card totals
- Blackjack detection and game state tracking
- Professional formatting for terminal-based gameplay

Author: Artiom Lisin
"""

from typing import List

from blackjack_deck import Card
from hand import Hand


class Player(Hand):
    """
    Player class extending Hand with betting and status display features.
    
    This class represents a blackjack player with betting capabilities,
    bankroll management, and enhanced display formatting. It maintains
    all hand functionality while adding game-specific features like
    betting, status tracking, and professional output formatting.
    
    Attributes:
        player_name (str): Player's display name
        money_pool (float): Player's current bankroll/money
        can_split (bool): Whether player can split their hand
        bankrupt (bool): Whether player has run out of money
        is_bust (bool): Whether player's hand has busted (>21)
        
    Note:
        Player inherits all hand management from the Hand class,
        including card value calculation and ace handling.
    """

    def __init__(self, player_name: str, player_bank: float, player_initial_draw: List[Card]):
        """
        Initialize a player with name, bankroll, and initial cards.
        
        Args:
            player_name (str): Display name for the player
            player_bank (float): Starting bankroll amount
            player_initial_draw (List[Card]): Initial 2-card hand
            
        Raises:
            ValueError: If player_bank is not positive
            ValueError: If player_initial_draw doesn't contain 2 cards (inherited)
            
        Note:
            Automatically checks for split opportunities and bankruptcy status
            after initialization based on the initial cards and bankroll.
        """
        if player_bank <= 0:
            raise ValueError("playerBank must be positive and nonzero")
            
        # Initialize hand with parent class
        super().__init__(player_initial_draw)
        
        # Initialize player-specific attributes
        self.player_name = player_name
        self.money_pool = player_bank
        self.can_split = False
        self.bankrupt = False
        self.is_bust = False
        
        # Check initial game conditions
        self.check_split_hand()

    def bet_to_pot(self, bet: float) -> float:
        """
        Place a bet, handling all-in scenarios and bankruptcy checks.
        
        Processes a betting request, automatically checking for bankruptcy
        and handling cases where the bet exceeds available funds by going all-in.
        
        Args:
            bet (float): Requested bet amount
            
        Returns:
            float: Actual bet amount placed (may be less than requested for all-in)
            
        Note:
            If bet exceeds available funds, player automatically goes all-in.
            Bankruptcy status is checked before processing the bet.
            
        Example:
            >>> player.money_pool = 50
            >>> actual_bet = player.bet_to_pot(100)  # Goes all-in for 50
        """
        self.check_bankruptcy()
        
        if bet >= self.money_pool and not self.bankrupt:
            # Player is going all-in
            bet = self.money_pool
            print(f"{self.player_name} is now all in. Bet value: {bet}")
            
        self.money_pool -= bet
        return bet

    def check_bankruptcy(self) -> None:
        """
        Check and update the player's bankruptcy status.
        
        Evaluates whether the player has sufficient funds to continue playing.
        Updates the bankruptcy flag and displays appropriate messages.
        
        Note:
            A player is considered bankrupt when money_pool <= 0.
            This method updates the bankrupt flag and provides user feedback.
        """
        if self.money_pool <= 0:
            self.bankrupt = True
            print(f"{self.player_name} is bankrupt.")
        else:
            self.bankrupt = False

    def check_split_hand(self) -> None:
        """
        Check if the current hand is eligible for splitting.
        
        Determines whether the player can split their hand based on having
        exactly 2 cards of the same value. Updates the can_split flag accordingly.
        
        Split Rules:
        - Must have exactly 2 cards
        - Both cards must have the same value
        - Typically only allowed on initial deal
        
        Note:
            This method updates the can_split attribute based on current hand state.
            Split functionality would need additional implementation in the game logic.
        """
        if (len(self.current_hand) >= 2 and 
            self.current_hand[0].value == self.current_hand[1].value):
            self.can_split = True
        else:
            self.can_split = False

    def show_status(self) -> None:
        """
        Display the player's comprehensive status information.
        
        Creates and prints a detailed, professionally formatted status display
        showing the player's current hand, values, bankroll, and game status.
        The display includes emojis and clear visual separation for readability.
        
        Display Elements:
        - Player name with decorative header
        - Current hand cards with suit information
        - Hand value(s) with ace flexibility notation
        - Available funds/bankroll
        - Current game status (Active, Bust, Bankrupt, Blackjack)
        
        Status Indicators:
        - 💥 BUST: Hand total exceeds 21
        - 💸 BANKRUPT: No money remaining
        - 🃏 BLACKJACK: Hand totals exactly 21
        - ✅ Active: Normal playing status
        
        Note:
            This method prints directly to console and doesn't return a value.
            For hands with aces, displays both possible totals (soft/hard).
        """
        print(f"\n{'─'*40}")
        print(f"   🎮 {self.player_name}'s Status")
        print(f"{'─'*40}")
        
        # Show hand with detailed card information
        hand_display = [f"{card.value} of {card.suit}" for card in self.current_hand]
        print(f"🎴 Hand: {' | '.join(hand_display)}")
        
        # Show hand values with ace handling
        hand_values = self.get_hand_value()
        if len(hand_values) == 1:
            print(f"🎯 Hand value: {hand_values[0]}")
        else:
            print(f"🎯 Hand values: {min(hand_values)}/{max(hand_values)}")
        
        # Show financial status
        print(f"💰 Available funds: ${self.money_pool}")
        
        # Show current game status with appropriate indicators
        if self.is_bust:
            print("💥 Status: BUST")
        elif self.bankrupt:
            print("💸 Status: BANKRUPT")
        elif 21 in hand_values:
            print("🃏 Status: BLACKJACK!")
        else:
            print("✅ Status: Active")
        
        print(f"{'─'*40}")
