import random

class Card():
    '''Each instance represents a card in play. Each card is referred to by a unique integer called
    its index. The card name is recoverable by calling the name() method.'''
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

    def name(self):
        '''Converts the unique card index into a name string. Note that the ace has the highest rank and the
        ranks of all other cards ahs been transposed by -1, this is to make evaluation of hands easier.'''
        card_rank = str((self.index // 4) + 1)
        card_suit = ''
    
        if card_rank == '13':
            card_rank = 'ace'
        elif card_rank == '12':
            card_rank = 'king'
        elif card_rank == '11':
            card_rank = 'queen'
        elif card_rank == '10':
            card_rank = 'jack'

        if self.index % 4 == 0:
            card_suit = 'hearts'
        elif self.index % 4 == 1:
            card_suit = 'diamonds'
        elif self.index % 4 == 1:
            card_suit = 'spades'
        else:
            card_suit = 'clubs'
    
        card_name = card_rank + ' of ' + card_suit
    
        return card_name

class Player():
    def name():
        None

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

print('hello')
cards = draw_cards(3)
for card in cards:
    print(card.name())
print(Card.cards_in_play)