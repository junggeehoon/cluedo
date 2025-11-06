# SUSPECTS = ['mustard', 'plum', 'green', 'peacock', 'scarlet', 'white']
# WEAPONS = ['dagger', 'candlestick', 'revolver', 'rope', 'lead_pipe', 'wrench']
# ROOMS = [
#     'library', 'hall', 'lounge', 'kitchen', 'dining_room',
#     'study', 'ballroom', 'conservatory', 'billiard_room'
# ]

SUSPECTS = ['1', '2', '3', '4', '5', '6']
WEAPONS = ['7', '8', '9', '10', '11', '12']
ROOMS = ['13', '14', '15', '16', '17', '18', '19', '20', '21']

ALL_CARDS = SUSPECTS + WEAPONS + ROOMS

# players = ['a', 'b', 'c', 'd', 'e', 'f'] # 6명

# f (5) 질문 c (2) 가 대답
# => a(0), b(1)

# a (0) 질문 d (3) 가 대답
# => b(1), c(2)


# # ===============================
# # 추리 기록 및 정보 갱신
# # ===============================
# def process_suggestion(self, suggester, responder, cards):
#     print(f"\n📘 {suggester}가 {cards}를 추리했고, {responder}가 답했습니다.")
#     self.history.append((suggester, cards, responder))
#
#     s_idx = self.player_names.index(suggester)
#     r_idx = self.player_names.index(responder)
#     num_players = len(self.player_names)
#
#     # — 질문자 다음부터 답변자 전까지의 플레이어는 카드 없음
#     idx = (s_idx + 1) % num_players
#     while idx != r_idx:
#         player = self.player_names[idx]
#         print(f"  - {player}는 이 카드들을 가지고 있지 않음.")
#         for card in cards:
#             self.info[card]['not-owned-by'].add(player)
#         idx = (idx + 1) % num_players
#
#     print(f"  - {responder}는 카드 중 최소 하나를 가지고 있음.")


# info = {
#     # Suspects
#     'mustard': {'owner': 'a', 'not-owned-by': {}},
#     'plum': {'owner': 'a', 'not-owned-by': {}},
#     'green': {'owner': None, 'not-owned-by': {'b'}},
#     'peacock': {'owner': None, 'not-owned-by': {}},
#     'scarlet': {'owner': None, 'not-owned-by': {}},
#     'white': {'owner': None, 'not-owned-by': {}},
#
#     # Weapons
#     'dagger': {'owner': 'a', 'not-owned-by': {}},
#     'revolver': {'owner': None, 'not-owned-by': {'b'}},
#     'candlestick': {'owner': 'a', 'not-owned-by': {}},
#     'rope': {'owner': None, 'not-owned-by': {}},
#     'lead_pipe': {'owner': None, 'not-owned-by': {}},
#     'wrench': {'owner': None, 'not-owned-by': {}},
#
#     # Rooms
#     'library': {'owner': 'a', 'not-owned-by': {}},
#     'hall': {'owner': 'a', 'not-owned-by': {'b'}},
#     'lounge': {'owner': 'c', 'not-owned-by': {}},
#     'kitchen': {'owner': None, 'not-owned-by': {}},
#     'dining_room': {'owner': None, 'not-owned-by': {}},
#     'study': {'owner': None, 'not-owned-by': {}},
#     'ballroom': {'owner': None, 'not-owned-by': {}},
#     'conservatory': {'owner': None, 'not-owned-by': {}},
#     'billiard_room': {'owner': None, 'not-owned-by': {}},
# }