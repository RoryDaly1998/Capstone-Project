from characters import character_list, hand_ranking_scores
from hand_eval import evaluate_hand_ranking, evaluate_pre_flop, solve_draws
from models import Card, Player, Table
import random
from testing import testing_setup

def bet(table, player, value):
    '''Handles the adding of money to the pot when a player bets.'''
    if player.stack >= value:
        print(f'{player.name} has bet {value}.')
        table.pot += value
        player.stack -= value
    else:
        print(f'{player.name} has bet {player.stack}.')
        table.pot += player.stack
        player.stack = 0

def cpu_turn(table, player, value):
    '''Makes a choice of betting or folding for the cpu. Uses different algorithms depending on pre-flop or post-flop.'''
    if table.street == 'pre-flop':
        evaluate_pre_flop(table, player)

        if player.score >= 5:
            bet(table, player, value)
        else:
            fold(table, player)
    else:
        player.score = 0
        hand_ranking = evaluate_hand_ranking(table, player)

        for element in hand_ranking:
            player.score += hand_ranking_scores.get(element)

        if table.street == 'flop':
            if player.score >= 20:
                bet(table, player, value)
            else:
                fold(table, player)
        elif table.street == 'turn':
            if player.score >= 30:
                bet(table, player, value)
            else:
                fold(table, player)
        elif table.street == 'river':
            if player.score >= 20:
                bet(table, player, value)
            else:
                fold(table, player)

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

def fold(table, player):
    '''Handles when a player folds out of a hand.'''
    print(f'{player.name} has folded.')
    player.folded = True
    table.num_folded += 1

def user_turn(table, player, value):
    '''Gives the user a choice between betting and folding. Carries the action out.'''
    print(f'Your pocket cards are: {player.pocket_cards}')
    print(f'The pot is {table.pot}.')
    player_action = input('Type \'bet\' or \'fold\' to take that action: ').lower()

    validate_player_action = False
    while validate_player_action == False:
        if player_action == 'bet' or player_action == 'fold':
            validate_player_action = True
        else:
            player_action = input('Incorrect input. Please try again.').lower()

    if player_action == 'bet':
        bet(table, player, value)
    else:
        fold(table, player)

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
    user.is_user = True
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

    return table, player_list, user

def hand(table, player_list):
    '''Plays out a single hand.'''
    ## Pre-flop.
    table.street = 'pre-flop'

    for player in player_list:
        player.pocket_cards = draw_cards(2)

        # Automatically takes the blind money and adds it to the pot.
        if player.order == 1:
            if player.stack >= table.small_blind:
                print(f'{player.name} is the small blind and has bet {table.small_blind}.')
                table.pot += table.small_blind
                player.stack -= table.small_blind
            else:
                print(f'{player.name} is the small blind and has bet {player.stack}.')
                table.pot += player.stack
                player.stack = 0
        elif player.order == 2:
            if player.stack >= table.big_blind:
                print(f'{player.name} is the big blind and has bet {table.big_blind}.')
                table.pot += table.big_blind
                player.stack -= table.big_blind
            else:
                print(f'{player.name} is the big blind and has bet {player.stack}.')
                table.pot += player.stack
                player.stack = 0

        # If the player is not one of the blinds they get to decide to bet or fold.
        elif player.is_user == True:
            user_turn(table, player, table.big_blind)

        # Runs the pre-flop hand evaluation algorithm to decide the actions of the CPU players.
        else:
            cpu_turn(table, player, table.big_blind)

    # Gives the small blind player the choice to bet or fold after everyone else has gone.
    for player in player_list:
        if player.order == 1:
            if player.is_user == True:
                user_turn(table, player, table.small_blind)
            else:
                cpu_turn(table, player, table.small_blind)

    ## Post-flop.
    post_flop_streets = ['flop', 'turn', 'river']

    i = 0
    while i <= 2:
        table.street = post_flop_streets[i]
        if table.street == 'flop':
            table.board = draw_cards(3)
        else:
            table.board += draw_cards(1)

        for player in player_list:
            if player.folded == False:
                if player.is_user == True:
                    print(f'The board is: {table.board}')
                    user_turn(table, player, table.big_blind)
                else:
                    cpu_turn(table, player, table.big_blind)
            else:
                continue

        i += 1

    ## Find hand winner.
    # For now only hand rankings matter and not the rank of the hand, so all flushes or straights are considered equal for example.
    player_hand_scores = []
    for player in player_list:
        if player.folded == False:
            player_hand_ranking = evaluate_hand_ranking(table, player)
            player.score = hand_ranking_scores.get(player_hand_ranking[0])
            player_hand_scores.append(player.score)
        else:
            player.score = 0

    winning_score = max(player_hand_scores)
    winners = []

    for player in player_list:
        if player.score == winning_score:
            winners.append(player)

    winner_chips = table.pot // len(winners)
    table.pot = 0

    for winner in winners:
        winner.stack += winner_chips

table, player_list, user = testing_setup()
print(table.small_blind, table.big_blind)
hand(table, player_list)