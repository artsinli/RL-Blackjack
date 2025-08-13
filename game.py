from enum import Enum
from typing import List

from blackjack_deck import BlackjackDeck, Card
from player import Player
from dealer import Dealer


class GameState(Enum):
    """Enumeration of possible game states."""
    BETTING = "betting"
    DEALING = "dealing"
    PLAYER_TURN = "player_turn"
    DEALER_TURN = "dealer_turn"
    SHOWDOWN = "showdown"
    ROUND_END = "round_end"

class Game:
    def __init__(self) -> None:
        self.deck = BlackjackDeck()
        self.main_pot = 0
        self.side_pot = 0
        self.last_action = "Setup"
        self.state = GameState.BETTING
        self.min_bet = 10  # Minimum bet amount
        self.max_bet = 100  # Maximum bet amount
        self.player_bets = {}  # Track each player's bet for the round
        self.players = [
            Player(f"Jack {i+1}", 200, self.deck.draw_card(2)) for i in range(3)
        ]
        # Initialize dealer with 2 cards
        self.dealer = Dealer(self.deck.draw_card(2))
        self.players_remaining = len(self.players)
        self.num_rounds = 0

    def launch_game(self) -> None:
        print("🎲 Welcome to Blackjack! 🎲")
        print("Goal: Get as close to 21 as possible without going over!")
        print("Dealer hits on soft 17. Good luck!")
        
        quit_game = False
        while not quit_game:
            print(f"\n{'🎯'*20}")
            print(f"         ROUND {self.num_rounds + 1}")
            print(f"{'🎯'*20}")
            
            # Betting phase
            self.state = GameState.BETTING
            self.show_game_state_header()
            self.handle_betting_round()
            
            # Check if any players are still in the game after betting
            active_players = [p for p in self.players if not p.is_bust and not p.bankrupt]
            if not active_players:
                print("❌ No players remaining in the game!")
                break
            
            # Show initial game status after betting
            self.state = GameState.PLAYER_TURN
            self.show_game_state_header()
            
            # Show dealer's initial status (with hole card hidden)
            print("\n🎰 DEALER'S INITIAL HAND")
            print("─" * 40)
            self.dealer.show_hand(hide_hole_card=True)
            
            self.show_game_status()
            
            # Check for dealer blackjack early (peek rule)
            if self.dealer.has_blackjack:
                print("\n🃏 Dealer has blackjack! Revealing...")
                self.dealer.reveal_hole_card()
                self.state = GameState.SHOWDOWN
                self.show_round_results()
                self.payout_winnings()
            else:
                # Player turns
                for player in self.players:
                    if player.is_bust or player.bankrupt:
                        continue  # Skip bust/bankrupt players
                    
                    print(f"\n{'─'*30}")
                    print(f"   {player.player_name}'s Turn")
                    print(f"{'─'*30}")
                    
                    # Show dealer status before player's turn
                    print("🎰 Dealer showing:")
                    self.dealer.show_hand(hide_hole_card=True)
                    
                    # Show player status
                    player.show_status()
                    
                    # Player action loop
                    while not player.is_bust:
                        action = self.get_player_action()
                        
                        if action == "1":  # Hit
                            self.hit(player)
                            # Add a small pause for readability
                            if not player.is_bust:
                                input("\nPress Enter to continue...")
                        elif action == "2":  # Stand
                            self.handle_pass(player)
                            break
                        elif action == "3":  # Quit
                            quit_game = True
                            break
                    
                    if quit_game:
                        break
                
                if quit_game:
                    break
                    
                # Dealer turn (only if any players are not bust)
                if self.any_players_not_bust():
                    self.state = GameState.DEALER_TURN
                    self.handle_dealer_turn()
                
                # Determine winners and show results
                self.state = GameState.SHOWDOWN
                self.show_game_state_header()
                self.show_round_results()
                
                # Payout winnings
                self.payout_winnings()
            
            # Check if game should continue
            if self.check_game_bust():
                print("\n🏁 All players are bankrupt! Game over!")
                quit_game = True
            else:
                # Ask if players want to continue
                continue_input = input("\n🎮 Continue to next round? (y/n): ").lower().strip()
                if continue_input == 'n':
                    quit_game = True
                else:
                    # Reset for next round
                    self.reset_round()
                
            self.num_rounds += 1
            
        print(f"\n🎊 Thanks for playing! You completed {self.num_rounds} rounds.")

    def get_player_action(self) -> str:
        """Get a valid action from the player with clear prompts."""
        while True:
            print("\n🎯 Choose your action:")
            print("1️⃣  Hit (draw another card)")
            print("2️⃣  Stand (keep current hand)")
            print("3️⃣  Quit game")
            
            action = input("Enter your choice (1-3): ").strip()
            if action in ["1", "2", "3"]:
                return action
            print("❌ Invalid input. Please enter 1, 2, or 3.")

    def hit(self, player: Player) -> None:
        self.last_action = "Hit"
        card = self.draw(1)[0]
        player.add_card(card)
        last = player.current_hand[-1]
        
        # Show the card drawn
        print(f"\n🎯 {player.player_name} draws: {last.value} of {last.suit}")
        
        # Show updated hand and values
        hand_display = [f"{card.value} of {card.suit}" for card in player.current_hand]
        print(f"🎴 Updated hand: {' | '.join(hand_display)}")
        
        # Show current hand values
        hand_values = player.get_hand_value()
        if len(hand_values) == 1:
            print(f"🎯 Current total: {hand_values[0]}")
        else:
            print(f"🎯 Current totals: {min(hand_values)}/{max(hand_values)}")
        
        # Check for bust or 21
        if all(v > 21 for v in hand_values):
            print("💥 BUST!")
        elif 21 in hand_values:
            print("🎉 21! Perfect!")
        
        self.check_if_bust(player)

    def draw(self, n: int) -> list[Card]:
        return self.deck.draw_card(n)

    def check_game_bust(self) -> bool:
        """Check if the game should end (all players bankrupt)."""
        return all(player.bankrupt for player in self.players)

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
        self.last_action = "Stand"
        
        # Show final hand when standing
        hand_values = player.get_hand_value()
        if len(hand_values) == 1:
            final_total = hand_values[0]
        else:
            # Use the best possible value (highest that doesn't bust)
            valid_values = [v for v in hand_values if v <= 21]
            if valid_values:
                final_total = max(valid_values)
            else:
                final_total = min(hand_values)  # All values bust, show the lowest
        
        print(f"\n🛑 {player.player_name} stands with {final_total}")
        if len(hand_values) > 1:
            print(f"   (Hand values: {min(hand_values)}/{max(hand_values)})")
        print("─" * 40)

    def handle_betting_round(self) -> None:
        """Handle the betting phase for all players."""
        print("💰 BETTING ROUND ".center(60, "="))
        print(f"💵 Minimum bet: ${self.min_bet} | Maximum bet: ${self.max_bet}")
        print("-" * 60)
        
        for player in self.players:
            if player.bankrupt:
                print(f"💸 {player.player_name} is bankrupt and cannot bet.")
                continue
                
            # Show player's money with better formatting
            print(f"\n👤 {player.player_name}")
            print(f"   💰 Available funds: ${player.money_pool}")
            
            # Get bet amount
            bet_amount = self.get_player_bet(player)
            if bet_amount > 0:
                actual_bet = player.bet_to_pot(bet_amount)
                self.main_pot += actual_bet
                self.player_bets[player.player_name] = actual_bet
                print(f"   ✅ {player.player_name} bets ${actual_bet}")
            else:
                print(f"   ❌ {player.player_name} folds this round.")
                player.is_bust = True  # Mark as out for this round
        
        print(f"\n💰 Total pot this round: ${self.main_pot}")
        print("="*60)

    def get_player_bet(self, player: Player) -> float:
        """Get a valid bet amount from the player."""
        max_possible_bet = min(self.max_bet, player.money_pool)
        
        if max_possible_bet < self.min_bet:
            print(f"   ⚠️  {player.player_name} doesn't have enough money for minimum bet (${self.min_bet})")
            return 0
        
        while True:
            try:
                bet_input = input(f"   💵 Enter bet amount (${self.min_bet}-${max_possible_bet}) or 0 to fold: $")
                bet_amount = float(bet_input)
                
                if bet_amount == 0:
                    return 0
                elif bet_amount < self.min_bet:
                    print(f"   ❌ Bet must be at least ${self.min_bet}")
                elif bet_amount > max_possible_bet:
                    print(f"   ❌ Bet cannot exceed ${max_possible_bet}")
                else:
                    return bet_amount
            except ValueError:
                print("   ❌ Please enter a valid number")

    def payout_winnings(self) -> None:
        """Distribute winnings based on round results."""
        print("\n" + "💸 PAYOUTS ".center(60, "="))
        
        total_paid_out = 0
        
        for player in self.players:
            if player.player_name not in self.player_bets:
                continue  # Player didn't bet this round
                
            bet_amount = self.player_bets[player.player_name]
            result = self.determine_winner(player)
            
            if result == "win":
                winnings = bet_amount * 2  # Player gets their bet back plus equal amount
                player.money_pool += winnings
                total_paid_out += winnings
                print(f"🎉 {player.player_name} wins ${winnings} (bet: ${bet_amount})")
            elif result == "push":
                player.money_pool += bet_amount  # Player gets their bet back
                total_paid_out += bet_amount
                print(f"🤝 {player.player_name} pushes - bet returned: ${bet_amount}")
            else:  # lose or bust
                print(f"❌ {player.player_name} loses bet: ${bet_amount}")
            
            # Update bankruptcy status
            player.check_bankruptcy()
        
        print(f"\n💰 Total paid out: ${total_paid_out}")
        print("="*60)

    def handle_dealer_turn(self) -> None:
        """Handle the dealer's turn according to blackjack rules."""
        print("\n" + "="*50)
        print("🎰 DEALER'S TURN")
        print("="*50)
        
        # Reveal hole card
        self.dealer.reveal_hole_card()
        
        # Check for dealer blackjack
        if self.dealer.has_blackjack:
            print("Dealer has blackjack! No additional cards needed.")
            return
        
        # Dealer hits according to rules
        while self.dealer.should_hit():
            print(f"\nDealer must hit (total: {self.dealer.get_best_hand_value()})")
            input("Press Enter to continue...")
            
            card = self.draw(1)[0]
            self.dealer.add_card(card)
            print(f"🎯 Dealer draws: {card.value} of {card.suit}")
            self.dealer.show_full_hand()
            
            if self.dealer.is_bust():
                print("\n💥 DEALER BUSTS!")
                break
        
        if not self.dealer.is_bust() and not self.dealer.has_blackjack:
            final_total = self.dealer.get_best_hand_value()
            print(f"\n🛑 Dealer stands with {final_total}")

    def show_game_state_header(self) -> None:
        """Show a clear header indicating the current game state."""
        state_messages = {
            GameState.BETTING: "💰 BETTING PHASE",
            GameState.DEALING: "🎴 DEALING CARDS", 
            GameState.PLAYER_TURN: "👤 PLAYERS' TURN",
            GameState.DEALER_TURN: "🎰 DEALER'S TURN",
            GameState.SHOWDOWN: "🏆 SHOWDOWN",
            GameState.ROUND_END: "📊 ROUND COMPLETE"
        }
        
        print("\n" + "="*60)
        print(f"   {state_messages.get(self.state, 'GAME IN PROGRESS')}")
        print("="*60)

    def determine_winner(self, player: Player) -> str:
        """Determine the outcome for a player against the dealer."""
        if player.is_bust:
            return "bust"
        
        player_best = self.get_best_hand_value(player.get_hand_value())
        dealer_best = self.dealer.get_best_hand_value()
        
        if self.dealer.is_bust():
            return "win"
        elif player_best > dealer_best:
            return "win"
        elif player_best == dealer_best:
            return "push"
        else:
            return "lose"

    def get_best_hand_value(self, hand_values: List[int]) -> int:
        """Get the best possible hand value (closest to 21 without going over)."""
        valid_values = [value for value in hand_values if value <= 21]
        if valid_values:
            return max(valid_values)
        else:
            return min(hand_values)  # All values are over 21, return the smallest

    def any_players_not_bust(self) -> bool:
        """Check if any players are still in the game (not bust)."""
        return any(not player.is_bust for player in self.players)

    def show_game_status(self) -> None:
        """Display current game status including dealer and all players."""
        print("\n" + "📊 GAME STATUS ".center(60, "="))
        
        # Show pot information
        if self.main_pot > 0:
            print(f"💰 Current Pot: ${self.main_pot}")
            print()
        
        # Show dealer status
        self.dealer.show_hand(hide_hole_card=(self.state == GameState.PLAYER_TURN))
        print()
        
        # Show all players in a clean table format
        print("👥 PLAYERS".center(60, "-"))
        for i, player in enumerate(self.players, 1):
            status_parts = []
            
            # Player status
            if player.bankrupt:
                status_parts.append("💸 BANKRUPT")
            elif player.is_bust:
                status_parts.append("💥 BUST")
            else:
                hand_values = player.get_hand_value()
                if len(hand_values) == 1:
                    status_parts.append(f"🎯 {hand_values[0]}")
                else:
                    status_parts.append(f"🎯 {min(hand_values)}/{max(hand_values)}")
            
            # Add bet information if player has bet this round
            if player.player_name in self.player_bets:
                bet_amount = self.player_bets[player.player_name]
                status_parts.append(f"💵 Bet: ${bet_amount}")
            
            # Add money
            status_parts.append(f"💰 ${player.money_pool}")
            
            print(f"{i}. {player.player_name:<12} | {' | '.join(status_parts)}")
        
        print("="*60)

    def show_round_results(self) -> None:
        """Display the results of the current round."""
        print("\n" + "🏆 ROUND RESULTS ".center(60, "="))
        
        # Show final dealer hand
        print("🎰 Final Dealer Hand:")
        self.dealer.show_full_hand()
        print()
        
        # Show each player's result
        print("📋 Player Results:")
        print("-" * 60)
        
        for player in self.players:
            if player.player_name not in self.player_bets:
                continue  # Player didn't participate this round
                
            result = self.determine_winner(player)
            bet_amount = self.player_bets[player.player_name]
            
            # Get player's best hand value for display
            if not player.is_bust:
                player_best = self.get_best_hand_value(player.get_hand_value())
            else:
                player_best = min(player.get_hand_value())
            
            # Format result with emojis
            outcome = ""
            money_change = ""
            
            if result == "bust":
                outcome = "💥 BUST - Lost!"
                money_change = f"-${bet_amount}"
            elif result == "win":
                outcome = "🎉 WIN!"
                money_change = f"+${bet_amount}"
            elif result == "push":
                outcome = "🤝 PUSH (Tie)"
                money_change = "$0"
            elif result == "lose":
                outcome = "❌ LOSE"
                money_change = f"-${bet_amount}"
            else:
                outcome = "❓ UNKNOWN"
                money_change = "$0"
            
            print(f"{player.player_name:<15} | Hand: {player_best:<3} | {outcome:<15} | {money_change}")
        
        print("="*60)

    def reset_round(self) -> None:
        """Reset game state for the next round."""
        # Reset player bust status
        for player in self.players:
            if not player.bankrupt:  # Only reset non-bankrupt players
                player.is_bust = False
                # Deal new cards
                player.current_hand = self.deck.draw_card(2)
                player.calc_hand_value()
        
        # Reset dealer
        self.dealer = Dealer(self.deck.draw_card(2))
        
        # Reset betting data
        self.main_pot = 0
        self.player_bets = {}
        
        # Reset game state
        self.state = GameState.BETTING
        self.players_remaining = len([p for p in self.players if not p.bankrupt])
        
        print("\nNew round starting...")