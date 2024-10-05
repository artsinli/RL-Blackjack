classdef(Abstract=true) Hand < handle
    properties 
        current_hand % this is a BlackjackDeck item 
        hand_value double
    end
    methods (Access = protected)
        function obj = Hand()
            obj.current_hand = struct('Suit', {}, 'Value', {}, 'BlackjackValue', {});
            obj.hand_value = 0;
        end
        
        % Cannot discard cards from the players hand, must keep
        function addCard(obj, card)
            obj.current_hand(end + 1) = card;  % Add card to hand
            % obj.hand_value = getHandValue(obj);
        end
    end
    methods (Abstract)
        getHandValue();
    end
end

