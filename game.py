from blackjack_deck import BlackjackDeck, Card
from player import Player


class Game:
    def __init__(self) -> None:
        self.deck = BlackjackDeck()
        self.main_pot = 0
        self.side_pot = 0
        self.last_action = "Setup"
        self.players = [
            Player(f"Jack {i+1}", 200, self.deck.draw_card(2)) for i in range(3)
        ]
        self.current_player: Player | None = None
        self.total_bust_amount = len(self.players)
        self.num_rounds = 0

    def launch_game(self) -> None:
        quit_game = False
        while not quit_game:
            for player in self.players:
                self.current_player = player
                action = input("What action do you wish to take\n 1- hit\n 2- raise\n 3- pass\n")
                if action == "1":
                    self.hit()
                elif action == "2":
                    print("Raise")
                elif action == "3":
                    print("pass")
            if not self.check_game_bust():
                quit_game = True
            self.num_rounds += 1
        print("Game is over.")
        print(f"{self.num_rounds} rounds played.")

    def hit(self) -> None:
        self.last_action = "Hit"
        card = self.draw(1)[0]
        self.current_player.add_card(card)
        last = self.current_player.current_hand[-1]
        print(f"{self.current_player.player_name} drew a {last.value} of {last.suit}")
        self.check_if_bust()

    def draw(self, n: int) -> list[Card]:
        return self.deck.draw_card(n)

    def check_game_bust(self) -> bool:
        return self.total_bust_amount > 0

    def check_if_bust(self) -> None:
        hand_value = self.current_player.get_hand_value()
        if all(v > 21 for v in hand_value) and not self.current_player.is_bust:
            self.total_bust_amount -= 1
            self.current_player.is_bust = True
            print(
                f"{self.current_player.player_name} is now bust. {self.total_bust_amount} players remaining."
            )
