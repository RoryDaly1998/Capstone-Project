class Card():
    '''Each instance represents a card in play. Each card is referred to by a unique integer called
    its index. The card is represented in the terminal by a rank and suit symbol.'''
    cards_in_play = []

    def __new__(cls, index):
        '''Only creates a new card instance if the same card does not exist.'''
        if index in cls.cards_in_play:
            return None
        else:
            return super().__new__(cls)

    def __init__(self, index):
        self.index = index

        Card.cards_in_play.append(index)

        card_rank_numerical = (index % 13) + 2
        self.rank_numerical = card_rank_numerical

        card_rank_string = str(card_rank_numerical)
        
        if card_rank_string == '14':
            card_rank_string = 'A'
        elif card_rank_string == '13':
            card_rank_string = 'K'
        elif card_rank_string == '12':
            card_rank_string = 'Q'
        elif card_rank_string == '11':
            card_rank_string = 'J'

        self.rank_string = card_rank_string

        card_suit = ''

        if self.index % 4 == 0:
            card_suit = '\033[31m\u2665\033[0m'
        elif self.index % 4 == 1:
            card_suit = '\033[31m\u2666\033[0m'
        elif self.index % 4 == 2:
            card_suit = '\u2660'
        else:
            card_suit = '\u2663'

        self.suit = card_suit

    def __repr__(self):
        '''Converts the unique card index into a name string. Note that the ace has the highest rank and the
        ranks of all other cards ahs been transposed by -1, this is to make evaluation of hands easier.'''
        return self.rank_string + self.suit

class Player():
    '''Each instance represents a player in the game.'''
    player_list = []

    def __init__(self, name):
        self.name = name
        self.stack = None
        self.order = None
        self.pocket_cards = None
        self.score = 0
        self.folded = None

        Player.player_list.append(name)

    def __repr__(self):
        return self.name

class Table():
    '''Creates a game object which represents the rules of the game.'''

    def __init__(self):
        self.num_players = None
        self.big_blind = None
        self.small_blind = None
        self.ante = None
        self.hand_number = None
        self.street = None
        self.board = None
        self.num_folded = 0