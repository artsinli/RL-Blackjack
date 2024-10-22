% PUT ALMOST ALL OF THIS UNDER THE HAND CLASS, bet, softhand and doubledown
% can stay under player as those aren't dealer related.

classdef Player < Hand
    %% PROPERTIES
    properties
        playerName
        MoneyPool
        canSplit
        bankrupt
    end
    %% CONSTRUCTORS
    methods
        function obj = Player(playerName, playerBank, playerInitalDraw)
            arguments
                playerName {mustBeText}
                playerBank {mustBePositive, mustBeNonzero}
                playerInitalDraw
            end
            % Initialize from the super class
            obj@Hand(playerInitalDraw);
            obj.MoneyPool = playerBank;
            obj.playerName = playerName;
            obj.checkSplitHand;
        end
    end
    % methods
    %     function update(obj)
    %         obj.checkBankruptcy;
    %         obj.calcHandValue;
    %     end
    % end
    %% GAME METHODS
    methods
        function value = betToPot(obj, bet)
            obj.checkBankruptcy();
            if bet >= obj.MoneyPool && ~obj.bankrupt
                bet = obj.MoneyPool;
                warning(obj.playerName + ' is now all in. Bet value: ' + bet);
            end
            obj.MoneyPool = obj.MoneyPool - bet;
            value = bet;
        end
    end
    methods(Access = private) 
        function checkBankruptcy(obj)
            if obj.MoneyPool <= 0 
                obj.bankrupt = true;
                disp(obj.playerName + ' is bankrupt.')
            else
                obj.bankrupt = false;
            end
        end
        function checkSplitHand(obj)
            if isequal(obj.current_hand(1),obj.current_hand(2))
                obj.canSplit = true;
            else
                obj.canSplit = false;
            end
        end
    end
end

