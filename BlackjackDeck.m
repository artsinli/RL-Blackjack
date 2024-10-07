classdef BlackjackDeck < Deck
    %% PROPERTIES
    properties(Access=private,Constant)
        % Taken from a blackjack source, usually the range dealers cut
        cut_range = [60 75];
    end
    %% CONSTRUCTOR
    methods
        function obj = BlackjackDeck(numDecks)
            arguments
                numDecks uint32 {mustBeInteger} = 6
            end
            obj@Deck();  

            % Replicate the deck to the number of copies 
            obj.deck = repmat(obj.deck,1,numDecks);
            obj.deck = obj.shuffleDeck();

            % Cutting the deck here
            cutval = randi(BlackjackDeck.cut_range);
            bottomCards = obj.deck(end-cutval+1:end);
            obj.discardPile = [obj.discardPile, bottomCards];
            obj.deck(end-cutval+1:end) = [];
        end        
    end
    %% PUBLIC METHODS
    methods
        function draw = drawCard(obj,numCards)
            if nargin == 1
                numCards = 1;
            end
            draw = drawCard@Deck(obj,numCards);
            draw = arrayfun(@(card) setfield(card, 'BlackjackValue', obj.blackjackValue(card)), draw);
        end
    end
    %% PRIVATE METHODS
    methods (Access = private)
         function value = blackjackValue(~, card)
            switch card.Value
                case {'2', '3', '4', '5', '6', '7', '8', '9', '10'}
                    value = str2double(card.Value);  
                case {'Jack', 'Queen', 'King'}
                    % Face card blackjack value
                    value = 10;  
                case 'Ace'
                    % Ace can be worth 1 or 11
                    value = [1, 11];  
                otherwise
                    error('Invalid card value.');
            end
        end
    end
end