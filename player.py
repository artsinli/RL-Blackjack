from typing import List

from blackjack_deck import Card
from hand import Hand


class Player(Hand):
    def __init__(self, player_name: str, player_bank: float, player_initial_draw: List[Card]):
        if player_bank <= 0:
            raise ValueError("playerBank must be positive and nonzero")
        super().__init__(player_initial_draw)
        self.player_name = player_name
        self.money_pool = player_bank
        self.can_split = False
        self.bankrupt = False
        self.is_bust = False
        self.check_split_hand()

    def bet_to_pot(self, bet: float) -> float:
        self.check_bankruptcy()
        if bet >= self.money_pool and not self.bankrupt:
            bet = self.money_pool
            print(f"{self.player_name} is now all in. Bet value: {bet}")
        self.money_pool -= bet
        return bet

    def check_bankruptcy(self) -> None:
        if self.money_pool <= 0:
            self.bankrupt = True
            print(f"{self.player_name} is bankrupt.")
        else:
            self.bankrupt = False

    def check_split_hand(self) -> None:
        if len(self.current_hand) >= 2 and self.current_hand[0].value == self.current_hand[1].value:
            self.can_split = True
        else:
            self.can_split = False

    def show_status(self) -> None:
        """Display the player's current status including hand, hand value(s), and money."""
        print(f"\n{'─'*40}")
        print(f"   🎮 {self.player_name}'s Status")
        print(f"{'─'*40}")
        
        # Show hand with card emojis
        hand_display = [f"{card.value} of {card.suit}" for card in self.current_hand]
        print(f"🎴 Hand: {' | '.join(hand_display)}")
        
        # Show hand values with better formatting
        hand_values = self.get_hand_value()
        if len(hand_values) == 1:
            print(f"🎯 Hand value: {hand_values[0]}")
        else:
            print(f"🎯 Hand values: {min(hand_values)}/{max(hand_values)}")
        
        # Show available money
        print(f"💰 Available funds: ${self.money_pool}")
        
        # Show status indicators
        if self.is_bust:
            print("💥 Status: BUST")
        elif self.bankrupt:
            print("💸 Status: BANKRUPT")
        elif 21 in hand_values:
            print("🃏 Status: BLACKJACK!")
        else:
            print("✅ Status: Active")
        
        print(f"{'─'*40}")
