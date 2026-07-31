def check_straight_sequence(integer_list, num_needed):
    '''From a given integer list find if there are num within 5 consecutive.'''
    for i in range(2, 9):
        if len(set(integer_list).intersection(set(range(i, i + 5)))) == num_needed:
            return True

    return False

def find_straight(table, player):
    '''Returns if the player has a straight or could get one.'''
    ranks_in_play = []
    for card in table.board:
        ranks_in_play.append(card.rank_numerical)
    for card in player.pocket_cards:
        ranks_in_play.append(card.rank_numerical)

    if table.street == 'turn':
        if check_straight_sequence(ranks_in_play, 5):
            return 'straight'
    elif table.street == 'river':
        if check_straight_sequence(ranks_in_play, 5):
            return 'straight'
        elif check_straight_sequence(ranks_in_play, 4):
            return '1 off straight'
    elif table.street == 'flop':
        if check_straight_sequence(ranks_in_play, 5):
            return 'straight'
        elif check_straight_sequence(ranks_in_play, 4):
            return '1 off straight'
        elif check_straight_sequence(ranks_in_play, 3):
            return '2 off straight'

def find_flush(table, player):
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

    cards_in_flush = []
    for card in (table.board + player.pocket_cards):
        if card.suit == max(suits_count, key=suits_count.get):
            cards_in_flush.append(card)

    if most_single_suit == 5:
        if check_straight_sequence(cards_in_flush, 5):  # Straight
            # Highest rank in the straight is an ace.
            if cards_in_flush[4] == 14:
                return 'royal flush'
            else:
                return 'straight flush'
        return 'flush'
    elif most_single_suit == 4:
        return '1 off flush'
    elif most_single_suit == 3:
        return '2 off flush'

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
    difference_between_ranks_ace_high = abs(
        cards[0].rank_numerical - cards[1].rank_numerical)
    difference_between_ranks_ace_low = abs(
        ((cards[0].rank_numerical - 1) % 13) - ((cards[1].rank_numerical - 1) % 13))
    difference_between_ranks = min(
        difference_between_ranks_ace_high, difference_between_ranks_ace_low)

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

def evaluate_hand_ranking(table, player):
    '''Returns the hand ranking for a player.'''
    hand_ranking = []

    table_cards_rank = []
    for card in table.board:
        table_cards_rank.append(card.rank_numerical)

    player_cards_rank = [player.pocket_cards[0].rank_numerical,
                         player.pocket_cards[1].rank_numerical]

    # Adds score if the player has a flush, straight or is close to one.
    if find_flush(table, player) == 'royal flush':
        hand_ranking.append('royal flush')
    elif find_flush(table, player) == 'straight flush':
        hand_ranking.append('straight flush')
    elif find_flush(table, player) == 'flush':
        hand_ranking.append('flush')
    elif find_straight(table, player) == 'straight':
        hand_ranking.append('straight')
    else:
        if find_flush(table, player) == '1 off flush' and (table.street == 'turn' or table.street == 'flop'):
            hand_ranking.append('1 off flush')
        elif find_straight(table, player) == '1 off straight' and (table.street == 'turn' or table.street == 'flop'):
            hand_ranking.append('1 off straight')
        elif find_flush(table, player) == '2 off flush' and table.street == 'flop':
            hand_ranking.append('2 off flush')
        elif find_straight(table, player) == '2 off straight' and table.street == 'flop':
            hand_ranking.append('2 off straight')

        # Adds score if the player has pair, two-pair, three of a kind, four of a kind, or full house with the board.
        if player_cards_rank[0] == player_cards_rank[1]:
            if table_cards_rank.count(player_cards_rank[0]) == 2:
                hand_ranking.append('four of a kind')
            elif table_cards_rank[0] == table_cards_rank[1] and table_cards_rank[1] == table_cards_rank[2]:
                hand_ranking.append('full house')
            elif table_cards_rank.count(player_cards_rank[0]) == 1:
                hand_ranking.append('three of a kind')
            elif len(table_cards_rank) > len(set(table_cards_rank)):
                hand_ranking.append('two pair')
            else:
                hand_ranking.append('pair')
        else:
            if table_cards_rank.count(player_cards_rank[0]) == 3 or table_cards_rank.count(player_cards_rank[1]) == 3:
                hand_ranking.append('four of a kind')
            elif ((table_cards_rank.count(player_cards_rank[0]) == 1 and table_cards_rank.count(player_cards_rank[1]) == 2)
                  or (table_cards_rank.count(player_cards_rank[0]) == 2 and table_cards_rank.count(player_cards_rank[1]) == 1)):
                hand_ranking.append('full house')
            elif table_cards_rank.count(player_cards_rank[0]) == 2 or table_cards_rank.count(player_cards_rank[1]) == 2:
                hand_ranking.append('three of a kind')
            elif table_cards_rank.count(player_cards_rank[0]) == 1 and table_cards_rank.count(player_cards_rank[1]) == 1:
                hand_ranking.append('two pair')
            elif table_cards_rank.count(player_cards_rank[0]) == 1 or table_cards_rank.count(player_cards_rank[1]) == 1:
                hand_ranking.append('pair')
            # Adds a score if the player has the high card in their hand.
            elif max(player_cards_rank) >= max(table_cards_rank):
                hand_ranking.append('high card')

    if len(hand_ranking) == 0:
        hand_ranking.append('nothing')

    return hand_ranking

def solve_draws(table, players):
    '''Takes a list of winning players who have the same hand ranking. Returns the result of the hand.'''
    hand_ranking = evaluate_hand_ranking(table, players[0])

    if hand_ranking == 'straight flush':
        for player in players:
            None

        cards = player.pocket_cards + table.board
        card_ranks = []
        card_suits = {}
        best_hand = []
        hand_rank = 0

        for card in cards:
            card_ranks.append(card.rank)
            if card.suit in card_suits:
                card_suits[f'card.suit'] += 1
            else:
                card_suits[f'card.suit'] = 1

        max_suit = max(card_suits.values())

        if max_suit >= 5:
            suit = card_suits.keys()[card_suits.values().index(max_suit)]

            for card in cards:
                if card.suit == suit:
                    best_hand.append(card)

            if len(best_hand) == 5:
                None

        else:
            return False
