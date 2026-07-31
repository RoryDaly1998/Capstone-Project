character_list = ['John', 'Anna', 'Phillip', 'Rachel', 'Terrence', 'Brenda', 'Will']

hand_ranking_scores = {
    'nothing': 0,
    '2 off straight': int((4 / 169) * 50),
    '2 off flush': int((1 / 16) * 60),
    '1 off straight': int((1 / 13) * 50),
    '1 off flush': int((1 / 4) * 60),
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