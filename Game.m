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
        end
    % REDO ALL                  
    end
    methods
        function g = LaunchGame(GAME)
            quitGame = false;
            % Loop through each play until exited
            while(~quitGame)
                for loopPlayer = GAME.players
                    GAME.currentPlayer = loopPlayer{1};
                    % GAME.currentPlayerID = id;
                    GAME.hit();
                end
                if ~GAME.checkGameBust()
                    quitGame = true;
                end
                if input("Quit Game?\n")==true || ~GAME.checkGameBust()
                    quitGame = true;
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
        function hit(GAME)
            GAME.lastAction = 'Hit';
            % GAME.players{GAME.currentPlayerID}.addCard(GAME.draw(1))
            GAME.currentPlayer.addCard(GAME.draw(1))
            GAME.checkIfBust();
        end
        function Raise(GAME)
        end
        function Fold(GAME)
        end
        
    end
    methods(Access = private)
        function value = draw(GAME,n)
            value = GAME.deck.drawCard(n);
        end

        % Currently inefficent, O(n) time as it has to check every player
        % and see if they are bust
        function value = checkGameBust(GAME)
            for i = 1:length(GAME.players)
                if ~GAME.players{i}.isBust
                    value = true;
                else
                    value = false;
                    break
                end
            end
        end

        function checkIfBust(GAME)
            if GAME.currentPlayer.handValue > 21
                GAME.currentPlayer.isBust = true;
                disp(GAME.currentPlayer.playerName + ' is now bust.');
            end
        end
    end

end

