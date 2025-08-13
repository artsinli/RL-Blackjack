"""
Blackjack Game - Main Entry Point

This module serves as the entry point for the Blackjack game application.
It initializes and launches the complete blackjack gaming experience with
betting, multiple players, and proper dealer mechanics.

Features:
- Multi-player blackjack gameplay
- Betting system with configurable limits
- Professional dealer with standard blackjack rules
- Enhanced UI with emojis and clear status displays
- Proper game state management

Author: Artiom Lisin
Repository: RL-Blackjack
"""

from game import Game


def main() -> None:
    """
    Create a Game instance and launch gameplay.
    
    This function initializes the blackjack game and starts the main game loop.
    The game includes betting rounds, player turns, dealer actions, and payouts
    following standard casino blackjack rules.
    """
    game = Game()
    game.launch_game()


if __name__ == "__main__":
    main()
