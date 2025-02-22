import random


def getCard(deck: list[any]) -> any:
    """
    You give this function a deck of cards, and it returns the first one for you.
    """
    return deck.pop()


def shuffle(deck: list[any]) -> list[any]:
    """
    You give this function a deck of cards, and it returns a shuffled copy of it.
    """
    _shuffled_deck = deck.copy()
    random.shuffle(_shuffled_deck)
    return _shuffled_deck


if __name__ == '__main__':

    SUITS = ('Spades', 'Hearts', 'Clubs', 'Diamonds')
    RANKS = ('Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King')

    NUMBER_CARDS = 8

    print('Welcome to Higher or Lower.')
    print('You have to choose whether the next card to be shown will be higher or lower than the current card.')
    print('Getting it right adds 20 points; get it wrong and you lose 15 points.')
    print('You have 50 points to start.\n')

    all_cards: list[dict[str, str | int]] = []
    for card_suit in SUITS:
        for card_value, card_rank in enumerate(RANKS):
            _card: dict[str, str | int] = {'rank': card_rank, 'suit': card_suit, 'value': card_value + 1}
            all_cards.append(_card)

    player_score: int = 50

    while True:
        print()
        game_deck: list[dict[str, str | int]] = shuffle(all_cards)
        current_card: dict[str, str | int] = getCard(game_deck)
        current_card_rank: str = current_card['rank']
        current_card_value: int = current_card['value']
        current_card_suit: str = current_card['suit']
        print(f'Starting card is : {current_card_rank} of {current_card_suit}\n')

        for cardNumber in range(0, NUMBER_CARDS):  # play one game of this many cards
            answer = input('Will the next card be higher or lower than the ' +
                           current_card_rank + ' of ' +
                           current_card_suit + '?  (enter h or l): ')
            answer = answer.casefold()  # force lower case
            nextCardDict = getCard(game_deck)
            nextCardRank = nextCardDict['rank']
            nextCardSuit = nextCardDict['suit']
            nextCardValue = nextCardDict['value']
            print('Next card is:', nextCardRank + ' of ' + nextCardSuit)

            if answer == 'h':
                if nextCardValue > current_card_value:
                    print('You got it right, it was higher')
                    player_score = player_score + 20
                else:
                    print('Sorry, it was not higher')
                    player_score = player_score - 15

            elif answer == 'l':
                if nextCardValue < current_card_value:
                    player_score = player_score + 20
                    print('You got it right, it was lower')

                else:
                    player_score = player_score - 15
                    print('Sorry, it was not lower')

            print('Your score is:', player_score)
            print()
            current_card_rank = nextCardRank
            current_card_value = nextCardValue
            current_card_suit = nextCardSuit

        goAgain = input('To play again, press ENTER, or "q" to quit: ')
        if goAgain == 'q':
            break

    print('OK bye')
