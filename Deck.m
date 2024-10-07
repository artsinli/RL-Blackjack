classdef(Abstract=true) Deck < handle
    %% PROPERTIES
    properties
        deck
        discardPile
    end
    properties(Constant)
        suits = {'Hearts', 'Diamonds', 'Clubs', 'Spades'};
        values = {'2', '3', '4', '5', '6', '7', '8', '9', '10', ...
            'Jack', 'Queen', 'King', 'Ace'};
    end
    %% CONSTRUCTOR
    methods (Access = protected)
        function obj = Deck()
            obj.deck = struct('Suit', {}, 'Value', {});
            obj.discardPile = struct('Suit', {}, 'Value', {});

            % Populate deck with all 52 cards
            for i = 1:length(Deck.suits)
                for j = 1:length(Deck.values)
                    card.Suit = Deck.suits{i};
                    card.Value = Deck.values{j};
                    obj.deck(end + 1) = card;
                end
            end
            obj.deck = obj.shuffleDeck();
        end
    end
    %% PUBLIC METHODS
    methods
        function drawnCard = drawCard(obj,numCards)
            if nargin == 1
                % A draw should default 1 card
                numCards = 1;
            end
            if isempty(obj.deck)
                error('No more cards in the deck.');
            end
            drawnCard = obj.deck(1:numCards);
            obj.deck(1:numCards) = [];
        end

        function shuffledDeck = shuffleDeck(obj)
            shuffledDeck = obj.deck(randperm(length(obj.deck)));
        end
        
        function discardCard(obj, cardIndex)
            if cardIndex > length(obj.deck)
                error('Card index out of range.');
            end
            discardedCard = obj.deck(cardIndex);
            obj.deck(cardIndex) = [];
            obj.discardPile = [obj.discardPile, discardedCard];
        end
        
        function displayDeck(obj)
            for i = 1:length(obj.deck)
                disp(['Card ' num2str(i) ': ' ...
                    obj.deck(i).Value ' of ' obj.deck(i).Suit]);
            end
        end
        
        function displayDiscardPile(obj)
            for i = 1:length(obj.discardPile)
                disp(['Discarded Card ' num2str(i) ': ' ...
                    obj.discardPile(i).Value ' of ' ...
                    obj.discardPile(i).Suit]);
            end
        end
    end
end