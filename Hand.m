classdef Hand < handle
    properties
        cards % this is a BlackjackDeck item 
    end
    properties
        hand_value
    end
    
    methods 
        function obj = Hand()
            obj.cards = struct('Suit', {}, 'Value', {}, 'BlackjackValue', {});
        end
        
        function addCard(obj, card)
            obj.cards(end + 1) = card;  % Add card to hand
            obj.hand_value = getHandValue(obj);
        end
    end
    
    methods (Access = private)
        function val = getHandValue(obj)
            val = 0;
            nAces = 0;
            for c = obj.cards
                if(size(c.BlackjackValue)>1)
                    nAces = nAces + 1;
                end
                val = val + c.BlackjackValue;
            end
            obj.hand_value = val;
        end
    end
end

