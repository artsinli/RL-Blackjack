classdef Player < Hand
    % PLAYERHAND The plays and rules associated with a player hand
    % Actions will be taken here as well
    properties
        bet
        AceTable
    end
    % May need to set to public so that a game class may use this 
    properties (Access = private)  
        and 
        nAces
        canDoubleDown 
        SoftHand 
    end
    %% CONSTRUCTORS
    methods
        function obj = Player(bet)
            % Initialize from the super class
            obj@Hand();

            % Beginning initialization
            obj.bet = bet;
            obj.SoftHand = false;
            obj.canDoubleDown = false;
            obj.nAces = 0;
        end

        function addCard(obj, card)
            % Must add cards to play
            addCard@Hand(obj,card);

            % Recalcs the hand value after each draw
            obj.calcHandValue;
        end
    end
    %% GET FUNCTIONS
    methods 
        function result = getHandValue(obj)
            obj.calcHandValue;
            % Recalculate at each run
            % obj.calcHandValue % Ensure up to date
            result = obj.hand_value;
        end
    end
    %% CALCULATION FUNCTIONS
    methods(Access = protected)
        function calcAceTable(obj)
            % Create an ace table, noting the hand_value for each high
            % chosen ace
            result = zeros([obj.nAces 2]);
            
            % From the first index (0 aces flipped) to nAces (max aces
            % flipped)
            for i = 0:obj.nAces
                result(i+1,:) = [i min(obj.hand_value) + 10*i];
            end
            obj.AceTable = result;
        end

        function calcHandValue(obj)
            % Reset the hand value and 
            % ace table to zero. Ensures there is no lingering
            % data or stacking.  
            obj.hand_value = 0; 
            obj.nAces = 0;
            for c = obj.current_hand
                obj.hand_value = obj.hand_value + c.BlackjackValue;
                if strcmp(c.Value,'Ace')
                    obj.nAces = obj.nAces + 1;
                end
            end
            if obj.nAces >= 1
                obj.calcAceTable();
            end
        end
    end
end

