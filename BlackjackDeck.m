classdef BlackjackDeck < Deck

    properties(Access=private,Constant)
        cut_range = [60 75];
    end

    methods
        % Constructor to call parent Deck constructor
        function obj = BlackjackDeck(numDecks)
            % Restricts the numDecks input variable to be an integer
            % with base value of 6.
            arguments
                numDecks uint32 {mustBeInteger} = 6 % default 6
            end
            obj@Deck();  % Call the constructor of the parent Deck class
            
            % Replicate the deck to the number of copies 
            obj.deck = repmat(obj.deck,1,numDecks);
          
            % Shuffle the combined deck
            obj.deck = obj.shuffleDeck();

            % Deck is then cut at the bottom,
            cutval = randi(BlackjackDeck.cut_range);
            
            bottomCards = obj.deck(end-cutval+1:end);

            obj.discardPile = [obj.discardPile, bottomCards];

            obj.deck(end-cutval+1:end) = [];
        end
     
        % Function to draw a card and get its Blackjack value
        function drawnCard = drawBlackjackCard(obj)
            drawnCard = obj.drawCard();  % Draw a card using the parent class method
            drawnCard.BlackjackValue = obj.blackjackValue(drawnCard);  % Get the Blackjack value of the card
        end
    end

    methods (Access = private)
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
    end
end