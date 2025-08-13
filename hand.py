from typing import List

from blackjack_deck import Card


class Hand:
    """Base hand class used for players."""

    def __init__(self, predraw: List[Card]):
        if len(predraw) < 2:
            raise ValueError("Must initiate a 2 card predraw to initialize a player")
        self.current_hand: List[Card] = list(predraw)
        self.hand_value: List[int] = []
        self.ace_table: List[tuple[int, int]] = []
        self.n_aces = 0
        self.calc_hand_value()

    def add_card(self, card: Card) -> None:
        self.current_hand.append(card)
        self.calc_hand_value()

    def get_hand_value(self) -> List[int]:
        self.calc_hand_value()
        return self.hand_value

    # protected-like methods
    def calc_ace_table(self) -> None:
        self.ace_table = [
            (i, self.hand_value[0] + 10 * i) for i in range(self.n_aces + 1)
        ]

    def calc_hand_value(self) -> None:
        self.n_aces = 0
        low_total = 0
        for card in self.current_hand:
            value = card.blackjack_value
            if isinstance(value, list):
                low_total += value[0]
                self.n_aces += 1
            else:
                low_total += value if value is not None else 0
        if self.n_aces:
            self.hand_value = [low_total, low_total + 10 * self.n_aces]
            self.calc_ace_table()
        else:
            self.hand_value = [low_total]
