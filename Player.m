classdef Player < Hand
    %% PROPERTIES
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
    end
    %% PUBLIC FUNCTIONS
    methods 
        function result = getHandValue(obj)
            % Recalculate at each run, 
            obj.calcHandValue;
            result = obj.hand_value;
        end

        function addCard(obj, card)
            % If no cards are added to player, obj.hand_value is 0
            addCard@Hand(obj,card);
            obj.calcHandValue;
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
            % Resets values for recalc
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

