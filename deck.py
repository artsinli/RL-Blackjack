from dataclasses import dataclass
from random import shuffle
from typing import List, Union


@dataclass
class Card:
    """Representation of a single playing card."""
    suit: str
    value: str
    blackjack_value: Union[int, List[int], None] = None


class Deck:
    """Generic deck of playing cards."""

    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    values = [
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "Jack",
        "Queen",
        "King",
        "Ace",
    ]

    def __init__(self) -> None:
        self.deck: List[Card] = [
            Card(suit, value) for suit in self.suits for value in self.values
        ]
        self.discard_pile: List[Card] = []
        self.shuffle_deck()

    def draw_card(self, num_cards: int = 1) -> List[Card]:
        """Draw one or more cards from the top of the deck."""
        if not self.deck:
            raise ValueError("No more cards in the deck.")
        drawn = self.deck[:num_cards]
        self.deck = self.deck[num_cards:]
        return drawn

    def shuffle_deck(self) -> List[Card]:
        """Shuffle the deck in place and return it."""
        shuffle(self.deck)
        return self.deck

    def discard_card(self, card_index: int) -> None:
        """Discard a card from the deck to the discard pile."""
        if card_index >= len(self.deck):
            raise IndexError("Card index out of range.")
        discarded = self.deck.pop(card_index)
        self.discard_pile.append(discarded)

    def display_deck(self) -> None:
        for i, card in enumerate(self.deck, 1):
            print(f"Card {i}: {card.value} of {card.suit}")

    def display_discard_pile(self) -> None:
        for i, card in enumerate(self.discard_pile, 1):
            print(f"Discarded Card {i}: {card.value} of {card.suit}")
