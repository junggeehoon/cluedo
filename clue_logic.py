import numpy as np
from itertools import product
from clue_data import ALL_CARDS, SUSPECTS, WEAPONS, ROOMS


def sort_suggestions(cards):
    def card_type(card):
        if card in SUSPECTS:
            return 0
        if card in WEAPONS:
            return 1
        return 2  # ROOMS

    return sorted(cards, key=card_type)


class ClueHelper:
    def __init__(self, players, my_name, my_cards):
        self.players = players
        self.num_players = len(players)
        self.my_name = my_name
        self.my_cards = set(my_cards)
        self.history = []  # 추리 기록 저장

        self.knowledge = {card: {'owner': None, 'not_owned_by': set()} for card in ALL_CARDS}

        # 내 카드 정보 업데이트
        for card in self.my_cards:
            self.knowledge[card]['owner'] = self.my_name

        other_cards = set(ALL_CARDS) - self.my_cards
        for card in other_cards:
            self.knowledge[card]['not_owned_by'].add(self.my_name)

        # 다른 모든 플레이어는 내 카드를 가지고 있지 않음
        other_players = set(self.players) - {self.my_name}
        for card in self.my_cards:
            self.knowledge[card]['not_owned_by'].update(other_players)

        # --- [1] 초기 확률 설정 (카테고리별 정규화)
        self.card_probs = {}

        # 용의자
        suspects_left = [s for s in SUSPECTS if s not in my_cards]
        suspect_prob = 1 / len(suspects_left)
        for s in SUSPECTS:
            self.card_probs[s] = 0 if s in my_cards else suspect_prob

        # 도구
        weapons_left = [w for w in WEAPONS if w not in my_cards]
        weapon_prob = 1 / len(weapons_left)
        for w in WEAPONS:
            self.card_probs[w] = 0 if w in my_cards else weapon_prob

        # 장소
        rooms_left = [r for r in ROOMS if r not in my_cards]
        room_prob = 1 / len(rooms_left)
        for r in ROOMS:
            self.card_probs[r] = 0 if r in my_cards else room_prob

    # ===============================
    # 📊 상태 표시
    # ===============================
    def display_status(self):
        # print(self.knowledge)

        for card in self.knowledge:
            print(
                f'{card}: owner { {self.knowledge[card]["owner"]} }, not_owned_by {self.knowledge[card]["not_owned_by"]}')

        print("\n===============================")
        print("현재 사건파일 후보 확률 (카테고리별 100%)")
        print("-------------------------------")

        def show(title, cards):
            print(f"\n[{title}]")
            for c in cards:
                print(f"{c:<15} : {self.card_probs[c] * 100:>5.2f}%")

        show("용의자", SUSPECTS)
        show("도구", WEAPONS)
        show("장소", ROOMS)
        print("===============================")

    def process_my_suggestion(self, suggester, suggestion_cards, shower, shown_card=None):
        # if shower:
        #     shown_card = input("  - 보여준 카드는 무엇인가요?: ")

        # 보여준 카드에 owner: shower 처리
        self.knowledge[shown_card]['owner'] = shower

        # 나(my_name)와 보여준 플레이어(shower) 사이에 있는 플레이어들은 추리한 카드 3장 모두 들고 있지 않다.
        suggester_idx = self.players.index(suggester)
        shower_idx = self.players.index(shower)

        idx = (suggester_idx + 1) % self.num_players

        while idx != shower_idx:
            # 질문자 다음부터 답변자 전까지의 플레이어
            player = self.players[idx]

            for card in suggestion_cards:
                self.knowledge[card]['not_owned_by'].add(player)
            idx = (idx + 1) % self.num_players

        # else:
        #     pass

    # 만약에 나도 카드를 안 들고 있고 나머지 플레이어들도 안 가지고 있으면 그 카드는 정답.

    def calculate_cases(self, suggestion_cards):
        cases = []
        sort_suggestions(suggestion_cards)
        for card in suggestion_cards:
            cases.append(len(self.players) - len(self.knowledge[card]['not_owned_by']) + 1)

        return cases

    def update_probabilities(self, shown_card):
        pass

    # # ===============================
    # # 📘 추리 기록
    # # ===============================
    #                             suggester, suggestion_cards, shower, shown_card
    # def record_suggestion(self, suggester, cards, shower=None, shown_card=None):
    #     self.history.append((suggester, cards, shower, shown_card))
    #     print(f"\n📘 추리 기록: {suggester} → {cards}, 보여준 사람: {shower}, 카드: {shown_card}")
    #     self.update_probabilities(cards, shower, shown_card)
    #
    # # ===============================
    # # 🧠 확률 갱신 로직 (카테고리별 정규화)
    # # ===============================
    # def update_probabilities(self, cards, shower, shown_card):
    #     weights = {card: 1.0 for card in cards}
    #
    #     # (1) 카드가 보여졌을 경우 → 사건파일 아닐 확률 = 0
    #     if shown_card:
    #         weights[shown_card] = 0.0
    #
    #     # (2) 아무도 안 보여줬다면 → 사건파일일 확률 강화
    #     elif not shower:
    #         for card in cards:
    #             weights[card] = 1.5  # 약 50% 강화
    #
    #     # (3) 보여준 사람은 있으나 카드 불명 → 변화 없음
    #     else:
    #         pass
    #
    #     # 확률 × 가중치 적용
    #     for card in cards:
    #         self.card_probs[card] *= weights[card]
    #
    #     # 카테고리별 정규화
    #     self.normalize_category(SUSPECTS)
    #     self.normalize_category(WEAPONS)
    #     self.normalize_category(ROOMS)
    #
    # # ===============================
    # # ⚖️ 카테고리별 정규화 함수
    # # ===============================
    # def normalize_category(self, category_cards):
    #     total = sum(self.card_probs[c] for c in category_cards)
    #     if total == 0:
    #         return
    #     for c in category_cards:
    #         self.card_probs[c] /= total
    #
    # # ===============================
    # # 🎯 다음 추리 추천
    # # ===============================
    # def recommend_move(self):
    #     s = max(SUSPECTS, key=lambda x: self.card_probs[x])
    #     w = max(WEAPONS, key=lambda x: self.card_probs[x])
    #     r = max(ROOMS, key=lambda x: self.card_probs[x])
    #
    #     print("\n🎯 추천 추리 조합:")
    #     print(f"용의자 → {s}")
    #     print(f"도구   → {w}")
    #     print(f"장소   → {r}")
