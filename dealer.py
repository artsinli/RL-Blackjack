from typing import List

from blackjack_deck import Card
from hand import Hand


class Dealer(Hand):
    """Dealer class for blackjack gameplay with clear state management."""

    def __init__(self, initial_cards: List[Card]):
        super().__init__(initial_cards)
        self.hole_card_hidden = True  # More descriptive name
        self.has_revealed = False
        # Don't check for blackjack here - cards don't have blackjack_value yet

    def _check_for_blackjack(self) -> bool:
        """Check if dealer has blackjack (21 with 2 cards)."""
        if len(self.current_hand) == 2:
            # Ensure cards have blackjack values assigned
            if all(card.blackjack_value is not None for card in self.current_hand):
                hand_values = self.get_hand_value()
                return 21 in hand_values
        return False

    @property
    def has_blackjack(self) -> bool:
        """Property to check for blackjack when accessed."""
        return self._check_for_blackjack()

    def reveal_hole_card(self) -> None:
        """Reveal the dealer's hole card (first card)."""
        if self.hole_card_hidden:
            self.hole_card_hidden = False
            self.has_revealed = True
            hole_card = self.current_hand[0]
            print(f"\n🎯 Dealer reveals hole card: {hole_card.value} of {hole_card.suit}")
            
            if self.has_blackjack:
                print("🃏 DEALER HAS BLACKJACK!")
            
            self.show_full_hand()

    def should_hit(self) -> bool:
        """
        Determine if dealer should hit based on standard blackjack rules.
        - Dealer hits on 16 or less
        - Dealer hits on soft 17 (Ace + 6)
        - Dealer stands on hard 17 or higher
        """
        if self.is_bust():
            return False
            
        hand_values = self.get_hand_value()
        
        # If dealer has blackjack, don't hit
        if self.has_blackjack:
            return False
        
        # Check for soft 17 (Ace counted as 11, total is 17)
        if 17 in hand_values and len(hand_values) > 1:
            # This is a soft 17, dealer must hit
            return True
        
        # Hit on 16 or less, stand on 17 or more
        return max(hand_values) < 17

    def show_hand(self, hide_hole_card: bool = True) -> None:
        """Display the dealer's hand with proper formatting."""
        if hide_hole_card and self.hole_card_hidden:
            self._show_hand_with_hidden_card()
        else:
            self.show_full_hand()

    def _show_hand_with_hidden_card(self) -> None:
        """Show dealer's hand with the first card hidden."""
        if len(self.current_hand) < 2:
            return
            
        visible_cards = self.current_hand[1:]
        card_display = ["🂠 [Hidden Card]"] + [f"{card.value} of {card.suit}" for card in visible_cards]
        
        print(f"🎰 Dealer's hand: {' | '.join(card_display)}")
        
        # Calculate visible value
        if visible_cards:
            visible_total = 0
            visible_aces = 0
            
            for card in visible_cards:
                value = card.blackjack_value
                if isinstance(value, list):
                    visible_total += value[0]
                    visible_aces += 1
                else:
                    visible_total += value if value is not None else 0
            
            if visible_aces > 0:
                high_total = visible_total + (10 * visible_aces)
                print(f"   🔍 Showing: {visible_total}/{high_total} (+ hidden card)")
            else:
                print(f"   🔍 Showing: {visible_total} (+ hidden card)")
        
        print(f"   ❓ Hidden card could be worth 1-11 points")

    def show_full_hand(self) -> None:
        """Show dealer's complete hand with values."""
        card_display = [f"{card.value} of {card.suit}" for card in self.current_hand]
        print(f"🎰 Dealer's hand: {' | '.join(card_display)}")
        
        hand_values = self.get_hand_value()
        if len(hand_values) == 1:
            print(f"   Dealer's total: {hand_values[0]}")
        else:
            # Show both values for hands with aces
            print(f"   Dealer's totals: {min(hand_values)}/{max(hand_values)}")
        
        # Show status
        if self.has_blackjack:
            print("   🃏 BLACKJACK!")
        elif self.is_bust():
            print("   💥 BUST!")
        elif not self.hole_card_hidden and not self.should_hit():
            best_value = self.get_best_hand_value()
            print(f"   🛑 Dealer stands with {best_value}")

    def is_bust(self) -> bool:
        """Check if dealer is bust (all hand values over 21)."""
        hand_values = self.get_hand_value()
        return all(value > 21 for value in hand_values)

    def get_best_hand_value(self) -> int:
        """Get the best possible hand value (closest to 21 without going over)."""
        hand_values = self.get_hand_value()
        valid_values = [value for value in hand_values if value <= 21]
        
        if valid_values:
            return max(valid_values)
        else:
            return min(hand_values)  # All values are over 21, return the smallest

    def get_status_summary(self) -> str:
        """Get a concise status summary for display."""
        if self.has_blackjack:
            return "BLACKJACK"
        elif self.is_bust():
            return "BUST"
        elif self.hole_card_hidden:
            return "Hidden card"
        else:
            best_value = self.get_best_hand_value()
            return f"Total: {best_value}"
