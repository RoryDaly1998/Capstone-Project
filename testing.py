from characters import character_list
from models import Player, Table
import random

def test_setup():
    user_name = 'user'
    num_players = 8
    starting_stack = 1000000
    big_blind = 1000
    small_blind = big_blind // 2
    ante = 0

    user = Player(user_name)
    player_list = []
    player_choice = random.sample(character_list, k=(num_players - 1))

    for i in range(len(player_choice)):
        player_list.append(Player(player_choice[i]))

    user_table_order = random.randint(1, num_players)
    player_list.insert(user_table_order - 1, user)

    for player in player_list:
        player.stack = starting_stack

    table = Table()
    table.big_blind = big_blind
    table.small_blind = small_blind
    table.ante = ante

    return table, player_list