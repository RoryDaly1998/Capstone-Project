from characters import character_list
from models import Card, Player, Table
import random
from testing import test_setup

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

def hand():
    '''Draws each player in the game a 2 card hand.'''
    for player in player_list:
        player.hand = draw_cards(2)

def setup():
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
    table.big_blind = big_blind
    table.small_blind = small_blind
    table.ante = ante

    return table, player_list

user_name = 'user'

table, player_list = test_setup()
print(table.big_blind, table.small_blind, table.ante)

hand()

for player in player_list:
    print(player.name, player.hand, player.stack)