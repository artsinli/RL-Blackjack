"""
Blackjack Game Engine

This module implements the main Game class that orchestrates a complete
blackjack game experience including betting, player/dealer turns, scoring,
and round management. It provides a full-featured terminal-based blackjack
game with casino-style rules and professional user interface.

Classes:
    GameState: Enumeration of possible game phases
    Game: Main game controller managing all blackjack gameplay

Features:
- Complete blackjack game loop with multiple rounds
- Professional betting system with configurable limits
- Standard casino dealer rules and player options
- Enhanced UI with emojis and clear status displays
- Comprehensive scoring and payout system
- Bankruptcy and game-over handling
- Round-by-round progression with reset functionality

Author: Artiom Lisin
"""

from enum import Enum
from typing import List

from blackjack_deck import BlackjackDeck, Card
from player import Player
from dealer import Dealer


class GameState(Enum):
    """
    Enumeration of possible game states in a blackjack round.
    
    This enum tracks the current phase of gameplay, allowing the game
    to properly manage UI displays, available actions, and game flow.
    
    States:
        BETTING: Players place their bets
        DEALING: Initial cards are being dealt
        PLAYER_TURN: Players make hit/stand decisions
        DEALER_TURN: Dealer plays according to house rules
        SHOWDOWN: Comparing hands and determining winners
        ROUND_END: Finalizing payouts and preparing for next round
    """
    BETTING = "betting"
    DEALING = "dealing"
    PLAYER_TURN = "player_turn"
    DEALER_TURN = "dealer_turn"
    SHOWDOWN = "showdown"
    ROUND_END = "round_end"


class Game:
    """
    Main blackjack game controller managing all aspects of gameplay.
    
    This class orchestrates a complete blackjack experience including
    multiple players, betting rounds, dealer mechanics, scoring, and
    game progression. It provides a professional casino-style game
    with proper blackjack rules and enhanced user interface.
    
    Attributes:
        deck (BlackjackDeck): Multi-deck blackjack deck for the game
        main_pot (int): Total money bet by all players this round
        side_pot (int): Reserved for future side bet functionality
        last_action (str): Description of the most recent game action
        state (GameState): Current phase of the game
        min_bet (int): Minimum allowed bet amount
        max_bet (int): Maximum allowed bet amount
        player_bets (dict): Mapping of player names to their current bets
        players (List[Player]): All players in the game
        dealer (Dealer): The house dealer
        players_remaining (int): Count of active (non-bankrupt) players
        num_rounds (int): Number of completed rounds
        
    Game Rules Implemented:
    - Standard blackjack scoring (21 is target, over 21 is bust)
    - Dealer hits on 16 or less, hits on soft 17
    - Player options: hit, stand
    - Betting with configurable limits
    - Bankruptcy detection and handling
    - Multiple rounds with reset functionality
    """

    def __init__(self) -> None:
        """
        Initialize a new blackjack game with default settings.
        
        Sets up the game environment with:
        - Fresh multi-deck blackjack deck
        - 3 players with starting bankrolls
        - Dealer with initial 2-card hand
        - Betting limits and game state
        - Initial card dealing for all participants
        
        Default Configuration:
        - 3 players with $200 starting bankroll each
        - Minimum bet: $10, Maximum bet: $100
        - Multi-deck shuffled blackjack deck
        - All participants start with 2-card hands
        """
        # Initialize game components
        self.deck = BlackjackDeck()
        self.main_pot = 0
        self.side_pot = 0  # Reserved for future side bets
        self.last_action = "Setup"
        self.state = GameState.BETTING
        
        # Betting configuration
        self.min_bet = 10   # Minimum bet amount
        self.max_bet = 100  # Maximum bet amount
        self.player_bets = {}  # Track each player's bet for the round
        
        # Initialize players with starting hands
        self.players = [
            Player(f"Jack {i+1}", 200, self.deck.draw_card(2)) for i in range(3)
        ]
        
        # Initialize dealer with 2-card hand
        self.dealer = Dealer(self.deck.draw_card(2))
        
        # Game state tracking
        self.players_remaining = len(self.players)
        self.num_rounds = 0

    def launch_game(self) -> None:
        """
        Launch the main game loop with welcome message and round management.
        
        This is the main entry point for the blackjack game, providing:
        - Welcome message and rules explanation
        - Round-by-round gameplay loop
        - Game state management and transitions
        - Bankruptcy checking and game termination
        - Player choice to continue or quit between rounds
        
        Game Flow:
        1. Display welcome and rules
        2. For each round:
           a. Betting phase
           b. Initial dealing and status display
           c. Check for dealer blackjack (early end)
           d. Player turns (hit/stand decisions)
           e. Dealer turn (if needed)
           f. Showdown and results
           g. Payout processing
        3. Check for game end conditions
        4. Offer continuation or exit
        
        Exit Conditions:
        - All players bankrupt
        - Player chooses to quit during action
        - Player chooses not to continue after round
        """
        # Welcome message and rules
        print("🎲 Welcome to Blackjack! 🎲")
        print("Goal: Get as close to 21 as possible without going over!")
        print("Dealer hits on soft 17. Good luck!")
        
        quit_game = False
        
        # Main game loop
        while not quit_game:
            # Round header
            print(f"\n{'🎯'*20}")
            print(f"         ROUND {self.num_rounds + 1}")
            print(f"{'🎯'*20}")
            
            # Phase 1: Betting
            self.state = GameState.BETTING
            self.show_game_state_header()
            self.handle_betting_round()
            
            # Check if any players are still active after betting
            active_players = [p for p in self.players if not p.is_bust and not p.bankrupt]
            if not active_players:
                print("❌ No players remaining in the game!")
                break
            
            # Phase 2: Initial game state display
            self.state = GameState.PLAYER_TURN
            self.show_game_state_header()
            
            # Show dealer's initial status (hole card hidden)
            print("\n🎰 DEALER'S INITIAL HAND")
            print("─" * 40)
            self.dealer.show_hand(hide_hole_card=True)
            
            self.show_game_status()
            
            # Phase 3: Check for dealer blackjack (early resolution)
            if self.dealer.has_blackjack:
                print("\n🃏 Dealer has blackjack! Revealing...")
                self.dealer.reveal_hole_card()
                self.state = GameState.SHOWDOWN
                self.show_round_results()
                self.payout_winnings()
            else:
                # Phase 4: Player turns
                for player in self.players:
                    if player.is_bust or player.bankrupt:
                        continue  # Skip inactive players
                    
                    # Player turn header
                    print(f"\n{'─'*30}")
                    print(f"   {player.player_name}'s Turn")
                    print(f"{'─'*30}")
                    
                    # Show current game state for player
                    print("🎰 Dealer showing:")
                    self.dealer.show_hand(hide_hole_card=True)
                    player.show_status()
                    
                    # Player action loop
                    while not player.is_bust:
                        action = self.get_player_action()
                        
                        if action == "1":  # Hit
                            self.hit(player)
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
                    
                # Phase 5: Dealer turn (if any players remain)
                if self.any_players_not_bust():
                    self.state = GameState.DEALER_TURN
                    self.handle_dealer_turn()
                
                # Phase 6: Showdown and results
                self.state = GameState.SHOWDOWN
                self.show_game_state_header()
                self.show_round_results()
                
                # Phase 7: Payout processing
                self.payout_winnings()
            
            # Check for game end conditions
            if self.check_game_bust():
                print("\n🏁 All players are bankrupt! Game over!")
                quit_game = True
            else:
                # Offer continuation
                continue_input = input("\n🎮 Continue to next round? (y/n): ").lower().strip()
                if continue_input == 'n':
                    quit_game = True
                else:
                    # Reset for next round
                    self.reset_round()
                
            self.num_rounds += 1
            
        # Game completion message
        print(f"\n🎊 Thanks for playing! You completed {self.num_rounds} rounds.")

    def get_player_action(self) -> str:
        """
        Get a valid action choice from the current player.
        
        Displays available actions and validates player input, ensuring
        only valid choices are accepted. Provides clear prompts and
        error handling for invalid inputs.
        
        Returns:
            str: Player's chosen action ("1" for hit, "2" for stand, "3" for quit)
            
        Available Actions:
        - Hit: Draw another card from the deck
        - Stand: Keep current hand and end turn
        - Quit: Exit the game immediately
        
        Note:
            This method loops until a valid input is received.
            Input validation prevents game errors from invalid choices.
        """
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
        """
        Process a player's hit action (draw another card).
        
        Draws a card from the deck, adds it to the player's hand,
        displays the new card and updated hand status, and checks
        for bust or perfect 21 conditions.
        
        Args:
            player (Player): The player requesting to hit
            
        Process:
        1. Draw one card from the deck
        2. Add card to player's hand (auto-calculates values)
        3. Display the drawn card
        4. Show updated hand with all cards
        5. Display current hand total(s)
        6. Check for bust or 21 conditions
        7. Update player's bust status if needed
        
        Output:
        - Card drawn announcement
        - Updated hand display with all cards
        - Current hand total(s) with ace handling
        - Special messages for bust or perfect 21
        """
        self.last_action = "Hit"
        
        # Draw and add card
        card = self.draw(1)[0]
        player.add_card(card)
        last_card = player.current_hand[-1]
        
        # Display drawn card
        print(f"\n🎯 {player.player_name} draws: {last_card.value} of {last_card.suit}")
        
        # Show updated complete hand
        hand_display = [f"{card.value} of {card.suit}" for card in player.current_hand]
        print(f"🎴 Updated hand: {' | '.join(hand_display)}")
        
        # Display current hand values with ace handling
        hand_values = player.get_hand_value()
        if len(hand_values) == 1:
            print(f"🎯 Current total: {hand_values[0]}")
        else:
            print(f"🎯 Current totals: {min(hand_values)}/{max(hand_values)}")
        
        # Check for special conditions
        if all(v > 21 for v in hand_values):
            print("💥 BUST!")
        elif 21 in hand_values:
            print("🎉 21! Perfect!")
        
        # Update player's bust status
        self.check_if_bust(player)

    def draw(self, n: int) -> list[Card]:
        """
        Draw cards from the game deck.
        
        Args:
            n (int): Number of cards to draw
            
        Returns:
            list[Card]: List of drawn cards
            
        Note:
            This is a convenience method that delegates to the deck's draw_card method.
            Cards are automatically removed from the deck when drawn.
        """
        return self.deck.draw_card(n)

    def check_game_bust(self) -> bool:
        """
        Check if the game should end due to all players being bankrupt.
        
        Returns:
            bool: True if all players are bankrupt, False if any can continue
            
        Note:
            This is used to determine if the game should terminate.
            A game ends when no players have money left to bet.
        """
        return all(player.bankrupt for player in self.players)

    def check_if_bust(self, player: Player) -> None:
        """
        Check if a player has busted and update game state accordingly.
        
        Evaluates the player's hand values and sets bust status if all
        possible values exceed 21. Updates remaining player count and
        provides feedback to other players.
        
        Args:
            player (Player): Player to check for bust condition
            
        Bust Logic:
        - Player is bust if ALL possible hand values exceed 21
        - Ace flexibility means multiple values must be checked
        - First bust detection triggers player elimination for round
        - Remaining player count is decremented
        
        Note:
            This method only triggers on the first bust detection per player.
            Once busted, player is out for the remainder of the round.
        """
        hand_value = player.get_hand_value()
        
        # Check if all possible hand values exceed 21
        if all(v > 21 for v in hand_value) and not player.is_bust:
            self.players_remaining -= 1
            player.is_bust = True
            print(
                f"{player.player_name} is now bust. {self.players_remaining} players remaining."
            )

    def handle_raise(self, player: Player) -> None:
        """
        Handle a player's raise action (placeholder for future implementation).
        
        Args:
            player (Player): Player attempting to raise
            
        Note:
            This method is a placeholder for future betting enhancements.
            Currently not implemented in the basic blackjack rules.
        """
        self.last_action = "Raise"
        # TODO: Implement raising/doubling down logic
        print(f"{player.player_name} raises (not implemented yet)")

    def handle_pass(self, player: Player) -> None:
        """
        Process a player's stand action (keep current hand).
        
        Finalizes the player's hand for the round, calculates the best
        possible hand value, and displays the final result with appropriate
        formatting for hands with multiple possible values (aces).
        
        Args:
            player (Player): Player choosing to stand
            
        Stand Processing:
        1. Calculate all possible hand values
        2. Determine best value (highest ≤21 or lowest if all bust)
        3. Display final hand total with ace notation if applicable
        4. Record stand action for game history
        
        Value Selection Logic:
        - If any values ≤21: Use highest valid value
        - If all values >21: Use lowest bust value
        - Display both values for ace hands for clarity
        """
        self.last_action = "Stand"
        
        # Calculate final hand value
        hand_values = player.get_hand_value()
        if len(hand_values) == 1:
            final_total = hand_values[0]
        else:
            # Choose best possible value (highest that doesn't bust)
            valid_values = [v for v in hand_values if v <= 21]
            if valid_values:
                final_total = max(valid_values)
            else:
                final_total = min(hand_values)  # All values bust, show lowest
        
        # Display stand decision and final value
        print(f"\n🛑 {player.player_name} stands with {final_total}")
        if len(hand_values) > 1:
            print(f"   (Hand values: {min(hand_values)}/{max(hand_values)})")
        print("─" * 40)

    def handle_betting_round(self) -> None:
        """
        Orchestrate the betting phase for all players.
        
        Manages the betting round by:
        - Displaying betting limits and pot information
        - Processing each player's bet in turn
        - Handling bankruptcy and folding
        - Accumulating bets into the main pot
        - Providing comprehensive betting status updates
        
        Betting Process:
        1. Display betting round header and limits
        2. For each player:
           a. Check bankruptcy status
           b. Display available funds
           c. Get bet amount (or fold decision)
           d. Process bet and update pot
           e. Record bet for payout calculations
        3. Display final pot total
        
        Special Handling:
        - Bankrupt players automatically skip betting
        - All-in scenarios are managed automatically
        - Folding players are marked as bust for the round
        - Bet validation ensures compliance with limits
        """
        print("💰 BETTING ROUND ".center(60, "="))
        print(f"💵 Minimum bet: ${self.min_bet} | Maximum bet: ${self.max_bet}")
        print("-" * 60)
        
        for player in self.players:
            if player.bankrupt:
                print(f"💸 {player.player_name} is bankrupt and cannot bet.")
                continue
                
            # Display player's financial status
            print(f"\n👤 {player.player_name}")
            print(f"   💰 Available funds: ${player.money_pool}")
            
            # Process bet
            bet_amount = self.get_player_bet(player)
            if bet_amount > 0:
                actual_bet = player.bet_to_pot(bet_amount)
                self.main_pot += actual_bet
                self.player_bets[player.player_name] = actual_bet
                print(f"   ✅ {player.player_name} bets ${actual_bet}")
            else:
                print(f"   ❌ {player.player_name} folds this round.")
                player.is_bust = True  # Mark as out for this round
        
        # Display final pot total
        print(f"\n💰 Total pot this round: ${self.main_pot}")
        print("="*60)

    def get_player_bet(self, player: Player) -> float:
        """
        Get a validated bet amount from a player with comprehensive input handling.
        
        Prompts the player for a bet amount within their financial constraints
        and the game's betting limits. Provides clear feedback for invalid
        inputs and handles edge cases like insufficient funds.
        
        Args:
            player (Player): Player placing the bet
            
        Returns:
            float: Valid bet amount, or 0 if player folds
            
        Validation Rules:
        - Must be numeric input
        - 0 is valid (represents folding)
        - Must meet minimum bet requirement
        - Cannot exceed maximum bet limit
        - Cannot exceed player's available funds
        - Automatic handling of insufficient funds for minimum bet
        
        Special Cases:
        - If player can't afford minimum bet, automatically returns 0
        - Clear error messages for each type of invalid input
        - Loops until valid input is received
        """
        # Calculate maximum possible bet for this player
        max_possible_bet = min(self.max_bet, player.money_pool)
        
        # Check if player can afford minimum bet
        if max_possible_bet < self.min_bet:
            print(f"   ⚠️  {player.player_name} doesn't have enough money for minimum bet (${self.min_bet})")
            return 0
        
        # Bet input loop with validation
        while True:
            try:
                bet_input = input(f"   💵 Enter bet amount (${self.min_bet}-${max_possible_bet}) or 0 to fold: $")
                bet_amount = float(bet_input)
                
                # Validate bet amount
                if bet_amount == 0:
                    return 0  # Player chooses to fold
                elif bet_amount < self.min_bet:
                    print(f"   ❌ Bet must be at least ${self.min_bet}")
                elif bet_amount > max_possible_bet:
                    print(f"   ❌ Bet cannot exceed ${max_possible_bet}")
                else:
                    return bet_amount  # Valid bet
                    
            except ValueError:
                print("   ❌ Please enter a valid number")

    def payout_winnings(self) -> None:
        """
        Distribute winnings to players based on round results.
        
        Calculates and distributes payouts for each player based on their
        performance against the dealer. Handles wins, losses, pushes, and
        busts with appropriate payout ratios and bankroll updates.
        
        Payout Structure:
        - Win: 2x bet (original bet + equal winnings)
        - Push (tie): 1x bet (original bet returned)
        - Loss/Bust: 0x bet (bet is lost)
        
        Process:
        1. Display payout header
        2. For each player with a bet:
           a. Determine round outcome vs dealer
           b. Calculate appropriate payout
           c. Update player's bankroll
           d. Display payout result
           e. Update bankruptcy status
        3. Display total payout summary
        
        Bankruptcy Update:
        - Automatically checks each player's financial status
        - Updates bankruptcy flags for future rounds
        - Provides clear feedback on financial changes
        """
        print("\n" + "💸 PAYOUTS ".center(60, "="))
        
        total_paid_out = 0
        
        # Process payout for each betting player
        for player in self.players:
            if player.player_name not in self.player_bets:
                continue  # Player didn't bet this round
                
            bet_amount = self.player_bets[player.player_name]
            result = self.determine_winner(player)
            
            # Calculate and distribute payout based on result
            if result == "win":
                winnings = bet_amount * 2  # Bet back + equal winnings
                player.money_pool += winnings
                total_paid_out += winnings
                print(f"🎉 {player.player_name} wins ${winnings} (bet: ${bet_amount})")
            elif result == "push":
                player.money_pool += bet_amount  # Bet returned
                total_paid_out += bet_amount
                print(f"🤝 {player.player_name} pushes - bet returned: ${bet_amount}")
            else:  # lose or bust
                print(f"❌ {player.player_name} loses bet: ${bet_amount}")
            
            # Update bankruptcy status after payout
            player.check_bankruptcy()
        
        print(f"\n💰 Total paid out: ${total_paid_out}")
        print("="*60)

    def handle_dealer_turn(self) -> None:
        """
        Execute the dealer's turn according to standard blackjack rules.
        
        Manages the dealer's play sequence including hole card reveal,
        blackjack checking, and automated hitting decisions. Follows
        strict casino rules with no player input required.
        
        Dealer Turn Sequence:
        1. Display dealer turn header
        2. Reveal hole card and show complete hand
        3. Check for dealer blackjack (early termination)
        4. If no blackjack, follow hitting rules:
           - Hit on 16 or less
           - Hit on soft 17
           - Stand on hard 17 or higher
        5. Continue until stand or bust
        6. Display final dealer result
        
        Dealer Rules Implemented:
        - Standard casino hole card reveal
        - Automatic blackjack detection
        - Soft 17 rule (dealer hits Ace+6)
        - Bust detection and handling
        - Clear status announcements for each action
        
        Note:
            This method handles all dealer actions automatically.
            No player input is required during the dealer's turn.
        """
        print("\n" + "="*50)
        print("🎰 DEALER'S TURN")
        print("="*50)
        
        # Step 1: Reveal hole card
        self.dealer.reveal_hole_card()
        
        # Step 2: Check for dealer blackjack
        if self.dealer.has_blackjack:
            print("Dealer has blackjack! No additional cards needed.")
            return
        
        # Step 3: Dealer hitting loop
        while self.dealer.should_hit():
            print(f"\nDealer must hit (total: {self.dealer.get_best_hand_value()})")
            input("Press Enter to continue...")
            
            # Draw card and add to dealer's hand
            card = self.draw(1)[0]
            self.dealer.add_card(card)
            print(f"🎯 Dealer draws: {card.value} of {card.suit}")
            self.dealer.show_full_hand()
            
            # Check for dealer bust
            if self.dealer.is_bust():
                print("\n💥 DEALER BUSTS!")
                break
        
        # Step 4: Final dealer status
        if not self.dealer.is_bust() and not self.dealer.has_blackjack:
            final_total = self.dealer.get_best_hand_value()
            print(f"\n🛑 Dealer stands with {final_total}")

    def show_game_state_header(self) -> None:
        """
        Display a clear header indicating the current game phase.
        
        Provides visual feedback about the current game state to help
        players understand what phase of the round is active. Uses
        consistent formatting and appropriate emojis for each state.
        
        Header Displays:
        - BETTING PHASE: When players place bets
        - DEALING CARDS: During initial card distribution
        - PLAYERS' TURN: When players make hit/stand decisions
        - DEALER'S TURN: When dealer plays automatically
        - SHOWDOWN: When comparing hands and determining winners
        - ROUND COMPLETE: When finalizing payouts and cleanup
        
        Note:
            This method uses the current GameState to determine the
            appropriate header message and formatting.
        """
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
        """
        Determine the outcome of a player's hand against the dealer.
        
        Compares player and dealer hands according to blackjack rules
        to determine the winner. Handles all possible outcomes including
        busts, ties, and standard comparisons.
        
        Args:
            player (Player): Player whose outcome to determine
            
        Returns:
            str: Outcome result ("win", "lose", "push", or "bust")
            
        Comparison Logic:
        1. If player is bust → "bust" (automatic loss)
        2. If dealer is bust and player not bust → "win"
        3. If player value > dealer value → "win"
        4. If player value = dealer value → "push" (tie)
        5. If player value < dealer value → "lose"
        
        Hand Value Selection:
        - Uses best possible hand value for each participant
        - Accounts for ace flexibility in value calculations
        - Follows standard blackjack comparison rules
        
        Note:
            This method only determines the outcome, not the payout amount.
            Payout calculations are handled separately in payout_winnings().
        """
        # Check for player bust first
        if player.is_bust:
            return "bust"
        
        # Get best hand values for comparison
        player_best = self.get_best_hand_value(player.get_hand_value())
        dealer_best = self.dealer.get_best_hand_value()
        
        # Determine outcome based on values
        if self.dealer.is_bust():
            return "win"  # Dealer bust, player wins
        elif player_best > dealer_best:
            return "win"  # Player has higher value
        elif player_best == dealer_best:
            return "push"  # Tie game
        else:
            return "lose"  # Dealer has higher value

    def get_best_hand_value(self, hand_values: List[int]) -> int:
        """
        Get the optimal hand value from a list of possible values.
        
        Selects the best possible hand value by choosing the highest
        value that doesn't exceed 21, or the lowest value if all
        values are over 21 (bust situation).
        
        Args:
            hand_values (List[int]): All possible hand values
            
        Returns:
            int: Best possible hand value
            
        Selection Algorithm:
        1. Filter for values ≤21 (valid values)
        2. If valid values exist, return the maximum
        3. If no valid values (all bust), return minimum
        
        Examples:
            - [7, 17] → 17 (best valid value)
            - [15, 25] → 15 (only valid value)
            - [22, 32] → 22 (lowest bust value)
            
        Note:
            This method is used for both player and dealer hand evaluation.
            It implements optimal blackjack hand value selection logic.
        """
        valid_values = [value for value in hand_values if value <= 21]
        
        if valid_values:
            # Return highest valid value (closest to 21 without busting)
            return max(valid_values)
        else:
            # All values are over 21 (bust), return the smallest
            return min(hand_values)

    def any_players_not_bust(self) -> bool:
        """
        Check if any players remain active in the round.
        
        Determines whether the dealer needs to play by checking if
        any players are still in the game (not busted). The dealer
        only plays if at least one player can still win.
        
        Returns:
            bool: True if any players are not bust, False if all are bust
            
        Note:
            This is used to determine if the dealer turn should be skipped.
            If all players are bust, dealer wins automatically without playing.
        """
        return any(not player.is_bust for player in self.players)

    def show_game_status(self) -> None:
        """
        Display comprehensive current game status for all participants.
        
        Provides a complete overview of the current game state including
        pot information, dealer status, and detailed player information
        in a clean, organized format with emojis and clear separators.
        
        Status Display Elements:
        1. Game status header
        2. Current pot amount (if active)
        3. Dealer hand status (hidden or revealed based on game state)
        4. Player summary table with:
           - Hand values (with ace flexibility)
           - Current bet amounts
           - Available bankroll
           - Status indicators (bust, bankrupt, blackjack, active)
        
        Player Status Indicators:
        - 💸 BANKRUPT: No money remaining
        - 💥 BUST: Hand exceeds 21
        - 🎯 X: Hand total (single value)
        - 🎯 X/Y: Hand totals (with aces)
        - 💵 Bet: Current bet amount
        - 💰 $X: Available funds
        
        Note:
            Display format adjusts based on current game state.
            Dealer hole card visibility depends on the current game phase.
        """
        print("\n" + "📊 GAME STATUS ".center(60, "="))
        
        # Show pot information if active
        if self.main_pot > 0:
            print(f"💰 Current Pot: ${self.main_pot}")
            print()
        
        # Show dealer status (context-sensitive)
        self.dealer.show_hand(hide_hole_card=(self.state == GameState.PLAYER_TURN))
        print()
        
        # Show player summary table
        print("👥 PLAYERS".center(60, "-"))
        for i, player in enumerate(self.players, 1):
            status_parts = []
            
            # Determine player status
            if player.bankrupt:
                status_parts.append("💸 BANKRUPT")
            elif player.is_bust:
                status_parts.append("💥 BUST")
            else:
                # Show hand values with ace handling
                hand_values = player.get_hand_value()
                if len(hand_values) == 1:
                    status_parts.append(f"🎯 {hand_values[0]}")
                else:
                    status_parts.append(f"🎯 {min(hand_values)}/{max(hand_values)}")
            
            # Add bet information if player has bet this round
            if player.player_name in self.player_bets:
                bet_amount = self.player_bets[player.player_name]
                status_parts.append(f"💵 Bet: ${bet_amount}")
            
            # Add current bankroll
            status_parts.append(f"💰 ${player.money_pool}")
            
            # Display formatted player line
            print(f"{i}. {player.player_name:<12} | {' | '.join(status_parts)}")
        
        print("="*60)

    def show_round_results(self) -> None:
        """
        Display comprehensive results for the completed round.
        
        Presents a detailed summary of the round outcome including
        final dealer hand, individual player results, and financial
        changes. Provides clear visual feedback for each participant's
        performance against the dealer.
        
        Results Display Structure:
        1. Round results header
        2. Final dealer hand with complete information
        3. Player results table showing:
           - Final hand values
           - Outcome vs dealer (win/lose/push/bust)
           - Financial impact (+/- bet amounts)
        
        Outcome Indicators:
        - 🎉 WIN: Player beat dealer
        - 🤝 PUSH: Tie with dealer
        - ❌ LOSE: Dealer beat player
        - 💥 BUST: Player exceeded 21
        
        Financial Display:
        - +$X: Money won (includes bet return + winnings)
        - $0: Push result (bet returned, no net change)
        - -$X: Money lost (bet amount)
        
        Note:
            Only shows results for players who participated in betting.
            Financial changes reflect the complete transaction (bet + winnings).
        """
        print("\n" + "🏆 ROUND RESULTS ".center(60, "="))
        
        # Show final dealer hand
        print("🎰 Final Dealer Hand:")
        self.dealer.show_full_hand()
        print()
        
        # Show individual player results
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
                player_best = min(player.get_hand_value())  # Show lowest bust value
            
            # Format result with appropriate indicators and financial impact
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
            
            # Display formatted result line
            print(f"{player.player_name:<15} | Hand: {player_best:<3} | {outcome:<15} | {money_change}")
        
        print("="*60)

    def reset_round(self) -> None:
        """
        Reset all game state for the next round while preserving player bankrolls.
        
        Prepares the game for a new round by resetting hands, game state,
        and betting information while maintaining player bankrolls and
        overall game progression. Handles bankruptcy by excluding bankrupt
        players from the new round.
        
        Reset Process:
        1. Reset player hands and bust status (non-bankrupt players only)
        2. Deal new 2-card hands to active players
        3. Reset dealer with new 2-card hand
        4. Clear betting round data (pot, individual bets)
        5. Reset game state to betting phase
        6. Update active player count
        
        Preservation:
        - Player bankrolls maintained from previous round
        - Player names and identities preserved
        - Game round counter continues incrementing
        - Overall game statistics maintained
        
        Exclusions:
        - Bankrupt players remain bankrupt (no reset)
        - Previous round betting data is cleared
        - Previous hands are discarded
        
        Note:
            This method is called between rounds to prepare for continued play.
            Only active (non-bankrupt) players receive new hands.
        """
        # Reset player states for active players
        for player in self.players:
            if not player.bankrupt:  # Only reset non-bankrupt players
                player.is_bust = False
                # Deal fresh 2-card hand
                player.current_hand = self.deck.draw_card(2)
                player.calc_hand_value()
        
        # Reset dealer with new hand
        self.dealer = Dealer(self.deck.draw_card(2))
        
        # Clear betting round data
        self.main_pot = 0
        self.player_bets = {}
        
        # Reset game state for new round
        self.state = GameState.BETTING
        self.players_remaining = len([p for p in self.players if not p.bankrupt])
        
        print("\nNew round starting...")