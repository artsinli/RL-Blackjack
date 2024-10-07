classdef(Abstract) Hand < handle
    %% PROPERTIES
    properties 
        % This is a BlackjackDeck item, TODO: force type
        current_hand
    end
    properties (Access = protected)
        hand_value
    end
    %% CONSTRUCTOR
    methods
        function obj = Hand()
            obj.current_hand = struct('Suit', {}, 'Value', {}, 'BlackjackValue', {});
        end
    end
    %% PUBLIC METHODS
    methods
        function addCard(obj, card)
            obj.current_hand = [obj.current_hand, card];
        end
    end
    %% ABSTRACT METHODS
    methods(Abstract, Access = protected)
        calcHandValue();
    end
end

