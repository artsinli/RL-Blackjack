classdef(Abstract) Hand < handle
    %% PROPERTIES
    properties(Access = public)
        current_hand
        hand_value
        AceTable
        nAces
        % SoftHand 
    end
    % Just in case the properties need to be protected
    % properties (Access = protected)
    %     current_hand
    %     hand_value
    %     AceTable
    %     nAces
    %     canDoubleDown 
    %     SoftHand 
    % end
    %% CONSTRUCTOR
    methods
        function obj = Hand(predraw)
            if length(predraw) < 2
                error(['Must initiate a 2 card predraw to ' ...
                    'initialize a player']);
            end
            obj.current_hand = predraw;    
            obj.nAces = 0;
            obj.calcHandValue;
        end
    end
    %% PUBLIC METHODS
    methods
        function addCard(obj, card)
            obj.current_hand = [obj.current_hand, card];
            obj.calcHandValue;
        end

        function result = getHandValue(obj)
            % Recalculate at each run
            obj.calcHandValue;
            result = obj.hand_value;
        end
    end
    %% ABSTRACT METHODS
    methods(Access = protected)
        % Calculates the different variations of having an ace or more than
        % 1 ace
        function calcAceTable(obj)
            % Create an ace table, noting the hand_value for each high
            % chosen ace
            result = zeros([obj.nAces 2]);
            
            % From the first index (0 aces flipped) to nAces (max aces
            % flipped)
            for i = 0:obj.nAces
                result(i+1,:) = [i, min(obj.hand_value) + 10*i];
            end
            obj.AceTable = result;
        end
        
        % Calculates range of high/low hand values. 
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

