classdef Game
    properties
        mainPot
        sidePot
        players
        deck
        currentPlayerID
        currentPlayer
        lastAction
    end
    methods
        function GAME = Game()
            %GAME Construct an instance of this class
            %   Detailed explanation goes here
            GAME.deck = BlackjackDeck();
            GAME.mainPot = 0;
            GAME.sidePot = 0;
            GAME.lastAction = 'Setup';
            
            for i = 1:3
                GAME.players{i} = Player("Jack " + i, ...
                    200,GAME.deck.drawCard(2));
            end
            
            % Order of player is order of initialization, with 1 being the
            % first player to go and length(players) being the last
            
        end
    % REDO ALL                  
    end
    methods
        function LaunchGame(GAME)
            quitGame = false;
            % Loop through each play until exited
            while(~quiteGame)
                for currentPlayer = GAME.Players
                end
            end
            disp('Game has ended.')
        end
        function debugGame(GAME)
            % Disp the current player
            disp('Current Player: ' + GAME.currentPlayer.playerName)
            disp('Hand Value Array: ')
            % Disp the hand value
            disp(GAME.currentPlayer.handValue)
            % Disp their action
            disp('Last Action: ')
            disp(GAME.lastAction)
        end
    end
    methods(Access = private)
        function Hit(GAME)
            GAME.lastAction = 'Hit';
            GAME.currentPlayer.addCard(GAME.Draw(1));
            if GAME.currentPlayer.handValue > 21
                GAME.currentPlayer.isBust = true;
            end
        end
        function Raise(GAME)
        end
        function Fold(GAME)
        end
        function CheckIfBust(GAME)
            for i = 1:length(GAME.players)
                player = GAME.players{i};
                if player.isBust == true
                    disp('Player ' + i + ' is now bust.');
                end
            end
        end
    end
    methods(Access = private)
        function value = Draw(GAME,n)
            value = GAME.deck.drawCard(n);
        end

    end

end

