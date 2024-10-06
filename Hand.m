classdef(Abstract) Hand < handle
    properties 
        current_hand % this is a BlackjackDeck item 
    end
    properties (Access = protected)
        hand_value
    end
    methods
        function obj = Hand()
            obj.current_hand = struct('Suit', {}, 'Value', {}, 'BlackjackValue', {});
            obj.hand_value = 0;
        end
        function addCard(obj, card)
            obj.current_hand = [obj.current_hand, card];
        end
    end
    methods(Abstract, Access = protected)
        calcHandValue();
    end
end

