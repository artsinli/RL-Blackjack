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
            %   Primary game class that is launched to play.
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
            % Loop through each play until exit
            while(~quitGame)
                for loopPlayer = GAME.players
                    GAME.currentPlayer = loopPlayer{1};

                    switch(input('What action do you wish to take\n 1- hit\n 2- raise \n 3- pass\n'))
                        case 1
                            GAME.hit()
                        case 2
                            fprintf("Raise\n")
                        case 3
                            fprintf("pass\n")
                    end
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
            fprintf(strcat(int2str(GAME.numRounds),' rounds played.\n'))
        end
        % function debugGame(GAME)
        %     % Disp the current player
        %     disp('Current Player: ' + GAME.currentPlayer.playerName)
        %     disp('Hand Value Array: ')
        %     % Disp the hand value
        %     disp(GAME.currentPlayer.handValue)
        %     % Disp their action
        %     disp('Last Action: ')
        %     disp(GAME.lastAction)
        % end
    end
    methods(Access = private)
        function hit(GAME)
            GAME.lastAction = 'Hit';
            GAME.currentPlayer.addCard(GAME.draw(1));
            fprintf(strcat(GAME.currentPlayer, " drew a ", ...
                GAME.currentPlayer.currentHand(end).))
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

        function value = checkGameBust(GAME)
            if GAME.totalBustAmount <= 0
                value = false;
            else
                value = true;
            end
        end

        function checkIfBust(GAME)
            if all(GAME.currentPlayer.handValue > 21)  ...
                    && ~GAME.currentPlayer.isBust

                GAME.totalBustAmount = GAME.totalBustAmount - 1;
                GAME.currentPlayer.isBust = true;
                disp(GAME.currentPlayer.playerName + ' is now bust. ' + ...
                    GAME.totalBustAmount + ' players remaining.\n');
            end
        end
    end

end

