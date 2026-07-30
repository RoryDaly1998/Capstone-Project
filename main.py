from characters import character_list
from helpers import is_sequence
from models import Card, Player, Table
import random
from testing import testing_setup

def draw_cards(num_to_draw):
    '''Draws a specified number of random cards. If a card is drawn which is already in play it
    will be forgotten and redrawn.'''
    num_drawn = 0
    cards = []

    while num_drawn < num_to_draw:
        card_index = random.randint(1, 52)
        card = Card(card_index)

        if card:
            num_drawn += 1
            cards.append(card)

    return cards

def evaluate_pre_flop(table, player):
    '''Simple hand evaluation algorithm for pre-flop.'''
    cards = player.pocket_cards

    # Gives the player's cards a score for how high their rank is.
    for card in cards:
        if card.rank_string == 'A':
            player.score += 8
        elif card.rank_string in ['K', 'Q', 'J']:
            player.score += 6
        elif card.rank_string in ['10', '9', '8']:
            player.score += 4
        elif card.rank_string in ['7', '6', '5']:
            player.score += 2
        else:
            player.score += 0

    # Gives the cards an extra score if they are suited.
    if cards[0].suit == cards[1].suit:
        player.score += 4

    # Gives the cards an extra score for how far away their rank is from each other. Need a special case here
    # because the ace can act as a high or low cards for straight purposes.
    difference_between_ranks_ace_high = abs(cards[0].rank_numerical - cards[1].rank_numerical)
    difference_between_ranks_ace_low = abs(((cards[0].rank_numerical - 1) % 13) - ((cards[1].rank_numerical - 1) % 13))
    difference_between_ranks = min(difference_between_ranks_ace_high, difference_between_ranks_ace_low)

    if difference_between_ranks == 0:
        player.score += 20
    elif difference_between_ranks == 1:
        player.score += 8
    elif difference_between_ranks == 2:
        player.score += 4
    elif difference_between_ranks == 3:
        player.score += 2
    elif difference_between_ranks == 4:
        player.score += 1

    # Lowers the score for each other active player in the hand.
    player.score -= 2 * (table.num_players - table.num_folded - 1)

def evaluate_post_flop(table, player):
    table_cards_rank = []
    for card in table.board:
        table_cards_rank.append(card.rank_numerical)

    player_cards_rank = [player.board[0].rank_numerical, player.board[1].rank_numerical]

    hand_scores = {
        'high card': 10,
        'pair': 20,
        'two pair': 30,
        'three of a kind': 40,
        'straight': 50,
        'flush': 60,
        'full house': 70,
        'four of a kind': 80,
        'straight flush': 90,
        'royal flush': 100
    }

    # Adds score if the player has the high card in their pocket cards.
    if max(player_cards_rank) >= max(table_cards_rank):
        player.score += hand_scores['high card']

    # Adds score if the player has pair, two-pair, three of a kind, four of a kind, or full house with the board.
    if player_cards_rank[0] == player_cards_rank[1]:
        if table_cards_rank.count(player_cards_rank[0]) == 2:
            player.score += hand_scores['four of a kind']
        elif table_cards_rank[0] == table_cards_rank[1] and table_cards_rank[1] == table_cards_rank[2]:
            player.score += hand_scores['full house']
        elif table_cards_rank.count(player_cards_rank[0]) == 1:
            player.score += hand_scores['three of a kind']
    else:
        if ((table_cards_rank.count(player_cards_rank[0]) == 1 and table_cards_rank.count(player_cards_rank[1]) == 2)
            or (table_cards_rank.count(player_cards_rank[0]) == 2 and table_cards_rank.count(player_cards_rank[1]) == 1)):
            player.score += hand_scores['full house']
        elif table_cards_rank.count(player_cards_rank[0]) == 2 or table_cards_rank.count(player_cards_rank[1]) == 2:
            player.score += hand_scores['three of a kind']
        elif table_cards_rank.count(player_cards_rank[0]) == 1 and table_cards_rank.count(player_cards_rank[1]) == 1:
            player.score += hand_scores['two pair']
        elif table_cards_rank.count(player_cards_rank[0]) == 1 or table_cards_rank.count(player_cards_rank[1]) == 1:
            player.score += hand_scores['pair']

    # Adds a score if the player has or is close to a straight or flush.
    def find_straight():
        '''Returns if the player has a straight or could get one.'''
        ranks_in_play = []
        for card in table.board:
            ranks_in_play.append(card.rank_numerical)
        for card in player.pocket_cards:
            ranks_in_play.append(card.rank_numerical)

        if table.street == 'turn':
            if is_sequence(ranks_in_play, 5):
                return 'straight'
        elif table.street == 'river':
            if is_sequence(ranks_in_play, 5):
                return 'straight'
            elif is_sequence(ranks_in_play, 4):
                return '1 off straight'
        elif table.street == 'flop':
            if is_sequence(ranks_in_play, 5):
                return 'straight'
            elif is_sequence(ranks_in_play, 4):
                return '1 off straight'
            elif is_sequence(ranks_in_play, 3):
                return '2 off straight'

    def find_flush():
        '''Returns if the player has a flush or could get one.'''
        suits_in_play = []
        for card in table.board:
            suits_in_play.append(card.suit)
        for card in player.pocket_cards:
            suits_in_play.append(card.suit)

        suits_count = {}
        for suit in suits_in_play:
            if suit in suits_count:
                suits_count[f'{suit}'] += 1
            else:
                suits_count[f'{suit}'] = 1

        most_single_suit = max(suits_count.values())

        if most_single_suit == 5:
            return 'flush'
        elif most_single_suit == 4:
            return '1 off flush'
        elif most_single_suit == 3:
            return '2 off flush'

    if table.street == 'river':
        if find_straight() == 'straight' and find_flush() == 'flush':
            player.score += hand_scores['straight flush']
        elif find_flush() == 'flush':
            player.score += hand_scores['flush']
        elif find_straight() == 'straight':
            player.score += hand_scores['straight']

    if table.street == 'turn':
        if find_flush() == 'flush':
            player.score += hand_scores['flush']
        elif find_straight() == 'straight':
            player.score += hand_scores['straight']
        elif find_flush() == '1 off flush':
            player.score += int(0.25 * hand_scores['flush'])
        elif find_straight() == '1 off straight':
            player.score += int((2 / 13) * hand_scores['straight'])

    if table.street == 'flop':
        if find_flush() == 'flush':
            player.score += hand_scores['flush']
        elif find_straight() == 'straight':
            player.score += hand_scores['straight']
        elif find_flush() == '1 off flush':
            player.score += int(0.25 * hand_scores['flush'])
        elif find_straight() == '1 off straight':
            player.score += int((2 / 13) * hand_scores['straight'])
        elif find_flush() == '2 off flush':
            player.score += int(0.0625 * hand_scores['flush'])
        elif find_straight() == '2 off straight':
            player.score += int((4 / 169) * hand_scores['straight'])

def hand():
    '''Draws each player in the game a 2 card hand.'''
    for player in player_list:
        player.pocket_cards = draw_cards(2)

def game_setup():
    '''Handles the setup for a new game. Gives the user options on the starting state of the game.'''
    # Asks the user for a name to refer to them and checks it does not conflict with any character names.
    user_name = input('What is your name? ')
    valid_user_name = False

    while valid_user_name == False:
        if user_name in character_list:
            user_name = input('That name is already taken, please choose another: ')
        else:
            valid_user_name = True

    # Asks the user how many players make up the game and make sure it is an integer no greater than 8.
    num_players = input('How many players are in the game, including you? (max 8) ')
    valid_num_players = False

    while valid_num_players == False:
        try:
            num_players = int(num_players)

            if num_players < 1 or num_players > 8:
                num_players = input('Please enter a valid number of players: ')
            else:
                valid_num_players = True
        except ValueError:
            num_players = input('Error. Your input must be an integer: ')

    # Create a list of all player objects in the new game and assigns them a random order at the table.
    user = Player(user_name)
    player_list = []
    player_choice = random.sample(character_list, k=(num_players - 1))

    for i in range(len(player_choice)):
        player_list.append(Player(player_choice[i]))

    user_table_order = random.randint(1, num_players)
    player_list.insert(user_table_order - 1, user)

    for index, player in enumerate(player_list):
        player.order = index + 1

    # Asks the user what the starting stack size should be and makes sure it is a positive integer.
    starting_stack = input('How many chips should each player start with? ')
    valid_starting_stack = False

    while valid_starting_stack == False:
        try:
            starting_stack = int(starting_stack)

            if starting_stack <= 0:
                starting_stack = input('Please type an integer greater than 0: ')
            else:
                for player in player_list:
                    player.stack = starting_stack

                valid_starting_stack = True
        except ValueError:
            starting_stack = input('Error. Your input must be an integer: ')

    # Asks the user what blind and ante rules should be used for the game.
    big_blind = input('What size big blind should the game have? (type 0 for none) ')
    valid_big_blind = False

    while valid_big_blind == False:
        try:
            big_blind = int(big_blind)
            small_blind = big_blind // 2

            if big_blind < 0:
                big_blind = input('Please type a non-negative integer: ')
            else:
                valid_big_blind = True
        except ValueError:
            big_blind = input('Error. Your input must be an integer: ')

    ante = input('What size ante should the game have? (type 0 for none) ')
    valid_ante = False

    while valid_ante == False:
        try:
            ante = int(ante)

            if ante < 0:
                ante = input('Please type a non-negative integer: ')
            else:
                valid_ante = True
        except ValueError:
            ante = input('Error. Your input must be an integer: ')

    # Create the game table object with the chosen rules.
    table = Table()
    table.num_players = num_players
    table.big_blind = big_blind
    table.small_blind = small_blind
    table.ante = ante

    return table, player_list

table, player_list = testing_setup()
print(table.big_blind, table.small_blind, table.ante)

hand()

for player in player_list:
    evaluate_pre_flop(table, player)
    print(player.name, player.pocket_cards, player.score)