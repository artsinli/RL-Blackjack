classdef Game
    properties
        mainPot
        sidePot
        players
        deck
    end
    methods
        function obj = Game()
            %GAME Construct an instance of this class
            %   Detailed explanation goes here
            obj.deck = BlackjackDeck();
            obj.mainPot = 0;
            obj.sidePot = 0;
            for i = 1:1
                obj.players{1} = Player("Jack",200,obj.deck.drawCard(2));
            end
        end
        
    end
    methods
        function GameRound(obj)
            Draw = @(n) obj.deck.drawCard(n);
            obj.players{1}.addCard(Draw(2))
        end
    end

end

