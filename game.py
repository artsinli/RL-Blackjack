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
        self.players_remaining = len(self.players)
        self.num_rounds = 0

    def launch_game(self) -> None:
        quit_game = False
        while not quit_game:
            for player in self.players:
                if player.is_bust:
                    continue  # Skip bust players
                
                player.show_status()
                
                # Input validation loop
                while True:
                    action = input("What action do you wish to take\n 1- hit\n 2- raise\n 3- pass\n 4- quit\n")
                    if action in ["1", "2", "3", "4"]:
                        break
                    print("Invalid input. Please enter 1, 2, 3, or 4.")
                
                if action == "1":
                    self.hit(player)
                elif action == "2":
                    self.handle_raise(player)
                elif action == "3":
                    self.handle_pass(player)
                elif action == "4":
                    quit_game = True
                    break
                    
            if self.check_game_bust():
                quit_game = True
            self.num_rounds += 1
        print("Game is over.")
        print(f"{self.num_rounds} rounds played.")

    def hit(self, player: Player) -> None:
        self.last_action = "Hit"
        card = self.draw(1)[0]
        player.add_card(card)
        last = player.current_hand[-1]
        print(f"{player.player_name} drew a {last.value} of {last.suit}")
        self.check_if_bust(player)

    def draw(self, n: int) -> list[Card]:
        return self.deck.draw_card(n)

    def check_game_bust(self) -> bool:
        return self.players_remaining == 0

    def check_if_bust(self, player: Player) -> None:
        hand_value = player.get_hand_value()
        if all(v > 21 for v in hand_value) and not player.is_bust:
            self.players_remaining -= 1
            player.is_bust = True
            print(
                f"{player.player_name} is now bust. {self.players_remaining} players remaining."
            )

    def handle_raise(self, player: Player) -> None:
        self.last_action = "Raise"
        # TODO: Implement betting logic
        print(f"{player.player_name} raises (not implemented yet)")

    def handle_pass(self, player: Player) -> None:
        self.last_action = "Pass"
        print(f"{player.player_name} passes")

    def deal(self) -> None:
        fo