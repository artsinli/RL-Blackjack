import random
from typing import List

from deck import Card, Deck


class BlackjackDeck(Deck):
    """Deck tailored for blackjack play."""

    deck_cut_range = (60, 75)

    def __init__(self, num_decks: int = 6) -> None:
        super().__init__()
        # replicate deck num_decks times
        single_deck = list(self.deck)
        self.deck = [Card(card.suit, card.value) for _ in range(num_decks) for card in single_deck]
        self.shuffle_deck()

        # cut the deck
        cutval = random.randint(*self.deck_cut_range)
        bottom_cards = self.deck[-cutval:]
        self.discard_pile.extend(bottom_cards)
        self.deck = self.deck[:-cutval]

    def draw_card(self, num_cards: int = 1) -> List[Card]:
        cards = super().draw_card(num_cards)
        for card in cards:
            card.blackjack_value = self.blackjack_value(card)
        return cards

    @staticmethod
    def blackjack_value(card: Card):
        if card.value in ["2", "3", "4", "5", "6", "7", "8", "9", "10"]:
            return int(card.value)
        if card.value in ["Jack", "Queen", "King"]:
            return 10
        if card.value == "Ace":
            return [1, 11]
        raise ValueError("Invalid card value.")
