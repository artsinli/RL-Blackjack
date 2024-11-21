classdef Game < handle
    properties
        mainPot
        sidePot
        players
        deck
        currentPlayerID
        currentPlayer
        lastAction
        totalBustAmount
    end
    properties
        numRounds
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
            GAME.totalBustAmount = length(GAME.players);
            GAME.numRounds = 0;
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
                % if input("Quit Game?\n")==true && quitGame == false
                %     quitGame = true;
                % end
                GAME.numRounds = GAME.numRounds + 1;
            end
            fprintf('Game is over.\n')
            fprintf(strcat(int2str(GAME.numRounds),' rounds played.'))
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
            if GAME.totalBustAmount <= 0
                value = false;
            else
                value = true;
            end
            % for i = 1:length(GAME.players)
            %     if ~GAME.players{i}.isBust
            %         value = true;
            %     else
            %         value = false;
            %         break
            %     end
            % end
        end

        function checkIfBust(GAME)
            % If the hand value with all combinations of aces is more than
            % 21, the player is considered bust. Not a RL agent specific
            % action so implemented on the game level. 
            if all(GAME.currentPlayer.handValue > 21)  ...
                    && ~GAME.currentPlayer.isBust

                GAME.totalBustAmount = GAME.totalBustAmount - 1;
                GAME.currentPlayer.isBust = true;
                disp(GAME.currentPlayer.playerName + ' is now bust. ' + ...
                    GAME.totalBustAmount + ' players remaining.');
            end
        end
    end

end

