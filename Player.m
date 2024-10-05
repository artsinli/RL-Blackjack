classdef Player < Hand
    % PLAYERHAND The plays and rules associated with a player hand
    % AActions can be taken here as well. 
    
    properties (Access = private)
        SoftHand 
        canDoubleDown 
        nAces 
    end
    methods
        function obj = Player()
            obj.SoftHand = false;
            obj.canDoubleDown = false;
        end
        function addCard(obj, card)
            addCard@Hand(obj,card);
        end
    end
end

