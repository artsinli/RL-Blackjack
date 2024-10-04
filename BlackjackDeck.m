classdef BlackjackDeck < Deck
    methods
        % Constructor to call parent Deck constructor
        function obj = BlackjackDeck(numDecks)
            arguments
                numDecks uint32 {mustBeInteger} = 6 % default 6
            end
            obj@Deck();  % Call the constructor of the parent Deck class
            if numDecks > 1
                for i = 2:numDecks
                    tempDeck = Deck();  % Create another instance of Deck
                    obj.deck = [obj.deck, tempDeck.deck];  % Concatenate the new deck
                end
                
                % Shuffle the combined deck
                obj.deck = obj.shuffleDeck();
            end
            
            % Shuffle the combined deck
            obj.deck = obj.shuffleDeck();
        end
        
        % Function to assign Blackjack value to a drawn card
        function value = blackjackValue(~, card)
            switch card.Value
                case {'2', '3', '4', '5', '6', '7', '8', '9', '10'}
                    value = str2double(card.Value);  % Convert numeric strings to numbers
                case {'Jack', 'Queen', 'King'}
                    value = 10;  % Face cards have a value of 10
                case 'Ace'
                    value = [1, 11];  % Ace can be worth 1 or 11
                otherwise
                    error('Invalid card value.');
            end
        end
        
        % Function to draw a card and get its Blackjack value
        function drawnCard = drawBlackjackCard(obj)
            drawnCard = obj.drawCard();  % Draw a card using the parent class method
            drawnCard.BlackjackValue = obj.blackjackValue(drawnCard);  % Get the Blackjack value of the card
        end
    end
end