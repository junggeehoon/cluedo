SUSPECTS = ['mustard', 'plum', 'green', 'peacock', 'scarlet', 'white']
WEAPONS = ['dagger', 'candlestick', 'revolver', 'rope', 'lead_pipe', 'wrench']
ROOMS = [
    'library', 'hall', 'lounge', 'kitchen', 'dining_room',
    'study', 'ballroom', 'conservatory', 'billiard_room'
]
ALL_CARDS = SUSPECTS + WEAPONS + ROOMS

players = ['a', 'b', 'c', 'd', 'e', 'f'] # 6명

# f (5) 질문 c (2) 가 대답
# => a(0), b(1)

# a (0) 질문 d (3) 가 대답
# => b(1), c(2)


info = {
    # Suspects
    'mustard': {'owner': 'a', 'not-owned-by': {}},
    'plum': {'owner': 'a', 'not-owned-by': {}},
    'green': {'owner': None, 'not-owned-by': {'b'}},
    'peacock': {'owner': None, 'not-owned-by': {}},
    'scarlet': {'owner': None, 'not-owned-by': {}},
    'white': {'owner': None, 'not-owned-by': {}},

    # Weapons
    'dagger': {'owner': 'a', 'not-owned-by': {}},
    'revolver': {'owner': None, 'not-owned-by': {'b'}},
    'candlestick': {'owner': 'a', 'not-owned-by': {}},
    'rope': {'owner': None, 'not-owned-by': {}},
    'lead_pipe': {'owner': None, 'not-owned-by': {}},
    'wrench': {'owner': None, 'not-owned-by': {}},

    # Rooms
    'library': {'owner': 'a', 'not-owned-by': {}},
    'hall': {'owner': 'a', 'not-owned-by': {'b'}},
    'lounge': {'owner': 'c', 'not-owned-by': {}},
    'kitchen': {'owner': None, 'not-owned-by': {}},
    'dining_room': {'owner': None, 'not-owned-by': {}},
    'study': {'owner': None, 'not-owned-by': {}},
    'ballroom': {'owner': None, 'not-owned-by': {}},
    'conservatory': {'owner': None, 'not-owned-by': {}},
    'billiard_room': {'owner': None, 'not-owned-by': {}},
}