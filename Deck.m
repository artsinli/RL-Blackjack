classdef(Abstract=true) Deck < handle
    properties
        deck         % Struct array representing the deck of cards
        discardPile  % Struct array representing the discard pile
    end

    properties(Constant)
        suits = {'Hearts', 'Diamonds', 'Clubs', 'Spades'};        % Struct array representing the deck of cards
        values = {'2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace'}; % Struct array representing the discard pile
    end

    methods (Access = protected)% Do not want access to this
        % Constructor to initialize deck
        function obj = Deck()
            % Initialize deck as an empty array
            obj.deck = struct('Suit', {}, 'Value', {});
            obj.discardPile = struct('Suit', {}, 'Value', {});
            
            % Populate deck with all 52 cards
            for i = 1:length(Deck.suits)
                for j = 1:length(Deck.values)
                    card.Suit = Deck.suits{i};
                    card.Value = Deck.values{j};
                    obj.deck(end + 1) = card;  % Add card to deck
                end
            end
            % Shuffle the deck
            obj.deck = obj.shuffleDeck();
        end

        
    end
    methods
        % Function to draw a card from the deck
        function drawnCard = drawCard(obj,numCards)
            if nargin == 1
                numCards = 1;
            end
            if isempty(obj.deck)
                error('No more cards in the deck.');
            end
            drawnCard = obj.deck(1:numCards);  % Draw the top card
            obj.deck(1) = [];  % Remove the card from the deck
        end

        % Function to shuffle the deck
        function shuffledDeck = shuffleDeck(obj)
            shuffledDeck = obj.deck(randperm(length(obj.deck)));
        end
        
        % Function to discard a card from the deck
        function discardCard(obj, cardIndex)
            if cardIndex > length(obj.deck)
                error('Card index out of range.');
            end
            
            % Remove the card from the deck
            discardedCard = obj.deck(cardIndex);
            obj.deck(cardIndex) = [];
            
            % Add the card to the discard pile
            obj.discardPile = [obj.discardPile, discardedCard];
        end
        
        % Function to display the deck
        function displayDeck(obj)
            for i = 1:length(obj.deck)
                disp(['Card ' num2str(i) ': ' obj.deck(i).Value ' of ' obj.deck(i).Suit]);
            end
        end
        
        % Function to display the discard pile
        function displayDiscardPile(obj)
            for i = 1:length(obj.discardPile)
                disp(['Discarded Card ' num2str(i) ': ' obj.discardPile(i).Value ' of ' obj.discardPile(i).Suit]);
            end
        end
    end
end