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

    def __repr__(self):
        '''Converts the unique card index into a name string. Note that the ace has the highest rank and the
        ranks of all other cards ahs been transposed by -1, this is to make evaluation of hands easier.'''
        card_rank = str(- (self.index // - 4))
        card_suit = ''

        if card_rank == '13':
            card_rank = 'A'
        elif card_rank == '12':
            card_rank = 'K'
        elif card_rank == '11':
            card_rank = 'Q'
        elif card_rank == '10':
            card_rank = 'J'

        if self.index % 4 == 0:
            card_suit = '\033[31m\u2665\033[0m'
        elif self.index % 4 == 1:
            card_suit = '\033[31m\u2666\033[0m'
        elif self.index % 4 == 2:
            card_suit = '\u2660'
        else:
            card_suit = '\u2663'

        card_name = card_rank + card_suit

        return card_name


class Table():
    '''Creates a game object which represents the rules of the game.'''

    def __init__(self):
        self.big_blind = None
        self.small_blind = None
        self.ante = None


class Player():
    '''Each instance represents a player in the game.'''
    player_list = []

    def __init__(self, name):
        self.name = name
        self.stack = None
        self.order = None
        self.hand = None

        Player.player_list.append(name)

    def __repr__(self):
        return self.name