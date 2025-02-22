import random

def getCard(deck: list[dict[str, str | int]]) -> dict[str, str | int]:
    """
    You give this function a deck of cards, and it returns the first one for you.
    """
    return deck.pop()

def shuffle(deck: list[dict[str, str | int]]) -> list[dict[str, str | int]]:
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
            _card = {'rank': card_rank, 'suit': card_suit, 'value': card_value + 1}
            all_cards.append(_card)

    player_score = 50

    while True:
        print()
        game_deck = shuffle(all_cards)
        current_card = getCard(game_deck)
        current_card_rank: str = current_card['rank']
        current_card_value: int = current_card['value']
        current_card_suit: str = current_card['suit']
        print(f'Starting card is : {current_card_rank} of {current_card_suit}\n')

        for round_of_game in range(0, NUMBER_CARDS):  # We will play 8 rounds of the game, by default
            answer = input(f'Will the next card be higher or lower than the {current_card_rank} of {current_card_suit}?  (enter h or l): ').casefold()

            next_card = getCard(game_deck)
            next_card_rank: str = next_card['rank']
            next_card_suit: str = next_card['suit']
            next_card_value: int = next_card['value']
            print(f'Next card is : {next_card_rank} of {next_card_suit}')

            if answer == 'h':
                if next_card_value > current_card_value:
                    print('You got it right, it was higher')
                    player_score += 20
                else:
                    print('Sorry, it was not higher')
                    player_score -= 15

            elif answer == 'l':
                if next_card_value < current_card_value:
                    player_score += 20
                    print('You got it right, it was lower')

                else:
                    player_score -= 15
                    print('Sorry, it was not lower')

            print(f'Your score is : {player_score}\n')
            current_card_rank = next_card_rank
            current_card_value = next_card_value
            current_card_suit = next_card_suit

        go_again = input('To play again, press ENTER, or "q" to quit: ')
        if go_again == 'q':
            break

    print('OK bye')
