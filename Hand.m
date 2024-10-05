classdef(Abstract) Hand < handle
    properties 
        current_hand % this is a BlackjackDeck item 
        hand_value double
    end
    methods
        function obj = Hand()
            obj.current_hand = struct('Suit', {}, 'Value', {}, 'BlackjackValue', {});
            obj.hand_value = 0;
        end
        % function obj = Hand(cards)
        %     obj.current_hand = cards;
        %     % MUST CALCULATE THE HAND VALUE AFTER
        
        % Cannot discard cards from the players hand, must keep
        function addCard(obj, card)
            obj.current_hand = [obj.current_hand, card];
        end
    end
end

