import numpy as np
from itertools import combinations, product

# --- 게임 기본 데이터 ---
SUSPECTS = ['머스타드', '플럼', '그린', '피콕', '스칼렛', '화이트']
WEAPONS = ['단검', '촛대', '권총', '밧줄', '파이프', '렌치']
ROOMS = ['서재', '홀', '라운지', '식당', '부엌', '연회장', '음악실', '온실', '당구장']
ALL_CARDS = SUSPECTS + WEAPONS + ROOMS


class ClueHelper:
    def __init__(self, num_players, player_names, my_name, my_cards):
        self.num_players = num_players
        self.players = player_names
        self.my_name = my_name
        self.my_cards = my_cards
        self.num_cards_per_player = (len(ALL_CARDS) - 3) // num_players

        # 지식 베이스 초기화
        # owner: 확정된 소유자
        # not_owned_by: 해당 카드를 가지고 있지 않음이 확인된 플레이어 집합
        self.knowledge = {card: {'owner': None, 'not_owned_by': set()} for card in ALL_CARDS}

        # "shower는 cards 중 하나를 가지고 있다"는 정보 저장
        self.possibility_sets = []

        # 내 카드 정보 업데이트
        for card in self.my_cards:
            self.knowledge[card]['owner'] = self.my_name

        # 다른 모든 플레이어는 내 카드를 가지고 있지 않음
        other_players = set(self.players) - {self.my_name}
        for card in self.my_cards:
            self.knowledge[card]['not_owned_by'].update(other_players)

    def record_suggestion(self, suggester, suggestion_cards, shower, shown_card=None):
        """
        게임에서 발생한 추리 활동을 기록합니다.
        - suggester: 추리한 사람
        - suggestion_cards: 추리에 사용된 카드 3장 리스트
        - shower: 카드를 보여준 사람 (없으면 None)
        - shown_card: 나에게 보여준 카드 (없으면 None)
        """
        print("\n[기록] 새로운 정보가 입력되었습니다. 추론을 시작합니다...")

        if shower is None:
            # 아무도 카드를 보여주지 않은 경우
            players_who_passed = set(self.players) - {suggester}
            for card in suggestion_cards:
                self.knowledge[card]['not_owned_by'].update(players_who_passed)
        elif shown_card:
            # shower가 나에게 카드를 보여준 경우
            self.knowledge[shown_card]['owner'] = shower
            # shower는 shown_card를 가지고 있으므로 다른 플레이어는 가질 수 없음
            other_players = set(self.players) - {shower}
            self.knowledge[shown_card]['not_owned_by'].update(other_players)
        else:
            # shower가 suggester에게 카드를 보여준 경우 (나는 무엇인지 모름)
            # 가능성 집합에 추가
            self.possibility_sets.append({
                'shower': shower,
                'suggester': suggester,
                'cards': set(suggestion_cards)
            })
            # suggester를 제외한 다른 플레이어들은 이 카드를 가지고 있지 않음
            # (shower부터 suggester까지 순서대로 확인했으므로)
            suggester_idx = self.players.index(suggester)
            shower_idx = self.players.index(shower)

            path_len = (shower_idx - suggester_idx - 1 + self.num_players) % self.num_players

            passed_players = []
            for i in range(1, path_len + 1):
                passed_players.append(self.players[(suggester_idx + i) % self.num_players])

            for card in suggestion_cards:
                self.knowledge[card]['not_owned_by'].update(passed_players)

        self.deduce()

    def deduce(self):
        """
        현재까지의 지식을 바탕으로 새로운 사실을 논리적으로 추론합니다.
        """
        changed = True
        while changed:
            changed = False

            # 1. 가능성 집합에서 정보 추론
            new_possibility_sets = []
            for p_set in self.possibility_sets:
                shower = p_set['shower']
                possible_cards = list(p_set['cards'])

                # 이미 주인이 밝혀졌거나, shower가 가질 수 없는 카드는 가능성에서 제거
                remaining_cards = [
                    c for c in possible_cards
                    if self.knowledge[c]['owner'] is None and shower not in self.knowledge[c]['not_owned_by']
                ]

                if len(remaining_cards) == 1:
                    # 남은 카드가 하나라면, 그 카드의 주인은 shower로 확정!
                    card_to_own = remaining_cards[0]
                    print(f"  [추론!] {shower}는 {card_to_own} 카드를 가지고 있음을 확신합니다.")
                    self.knowledge[card_to_own]['owner'] = shower
                    other_players = set(self.players) - {shower}
                    self.knowledge[card_to_own]['not_owned_by'].update(other_players)
                    changed = True
                elif len(remaining_cards) < len(p_set['cards']):
                    # 가능성이 줄어들었으면 갱신
                    p_set['cards'] = set(remaining_cards)
                    new_possibility_sets.append(p_set)
                    changed = True
                else:
                    new_possibility_sets.append(p_set)

            self.possibility_sets = new_possibility_sets

            # 2. 어떤 카드의 소유자가 아닌 사람이 n-1명이라면, 남은 1명이 소유자
            for card in ALL_CARDS:
                if self.knowledge[card]['owner'] is None:
                    possible_owners = set(self.players) - self.knowledge[card]['not_owned_by']
                    if len(possible_owners) == 1:
                        owner = possible_owners.pop()
                        print(f"  [추론!] 소거법에 의해 {owner}가 {card}의 주인입니다.")
                        self.knowledge[card]['owner'] = owner
                        changed = True

    def calculate_probabilities(self):
        """
        각 카드가 정답(봉투 속 카드)일 확률을 계산합니다.
        """
        probabilities = {}

        # 카테고리별로 정답 후보군 필터링
        solution_candidates = {
            'suspect': [s for s in SUSPECTS if self.knowledge[s]['owner'] is None],
            'weapon': [w for w in WEAPONS if self.knowledge[w]['owner'] is None],
            'room': [r for r in ROOMS if self.knowledge[r]['owner'] is None],
        }

        for category, candidates in solution_candidates.items():
            if not candidates: continue
            prob = 1.0 / len(candidates)
            for card in candidates:
                probabilities[card] = prob

        return probabilities, solution_candidates

    def recommend_move(self):
        """
        정보 획득을 최대화하는 최적의 추리를 추천합니다.
        """
        probabilities, candidates = self.calculate_probabilities()

        if not all(candidates.values()):
            print("\n[추천] 모든 카테고리의 정답 후보가 정해지지 않았습니다.")
            return

        best_suggestion = None
        max_score = -1

        # 모든 가능한 추리 조합 생성
        for suspect, weapon, room in product(candidates['suspect'], candidates['weapon'], candidates['room']):
            suggestion = (suspect, weapon, room)

            # 1. 기본 점수: 각 카드가 정답일 확률의 합 (가설 검증)
            score = probabilities.get(suspect, 0) + probabilities.get(weapon, 0) + probabilities.get(room, 0)

            # 2. 보너스 점수: 미해결 가능성 집합을 해결할 수 있는가 (미지 탐색)
            for p_set in self.possibility_sets:
                # 추리 카드와 가능성 집합의 교집합 크기만큼 보너스
                intersection = set(suggestion).intersection(p_set['cards'])
                if intersection:
                    score += 0.5 * len(intersection)  # 가중치 부여

            if score > max_score:
                max_score = score
                best_suggestion = suggestion

        print("\n--- ★ 다음 추리 추천 ★ ---")
        if best_suggestion:
            print(f"'{best_suggestion[0]}', '{best_suggestion[1]}', '{best_suggestion[2]}'")
            print(f"(예상 정보 획득 점수: {max_score:.2f})")
            print("이 조합은 현재 정답일 확률이 가장 높고, 다른 플레이어의 패에 대한 새로운 정보를 얻을 가능성이 큰 조합입니다.")
        else:
            print("추천할 조합을 찾을 수 없습니다.")

    def display_status(self):
        """
        현재까지 파악된 게임 상황을 출력합니다.
        """
        probabilities, _ = self.calculate_probabilities()

        print("\n" + "=" * 40)
        print("          현재 게임 추리 현황판")
        print("=" * 40)

        for category_name, category_cards in [("용의자", SUSPECTS), ("도구", WEAPONS), ("장소", ROOMS)]:
            print(f"\n--- {category_name} ---")
            for card in category_cards:
                info = self.knowledge[card]
                owner = info['owner']
                prob = probabilities.get(card, 0)

                if owner:
                    status = f"✅ 소유자: {owner}"
                else:
                    status = f"❔ 정답 확률: {prob:.1%}"

                print(f"{card:<8}: {status}")

        if self.possibility_sets:
            print("\n--- 미해결 정보 (Possibility Sets) ---")
            for i, p_set in enumerate(self.possibility_sets):
                cards_str = ", ".join(p_set['cards'])
                print(f"  {i + 1}. {p_set['shower']}는 {{ {cards_str} }} 중 하나를 가짐")

        print("=" * 40)


# --- 메인 프로그램 실행 함수 ---
def main():
    print("클루(Clue) 추리 보조 프로그램을 시작합니다.")

    # 1. 게임 설정
    num_players = int(input("총 플레이어 인원 수를 입력하세요: "))
    player_names = [input(f"플레이어 {i + 1}의 이름을 입력하세요 (시계방향 순서): ") for i in range(num_players)]
    my_name = input("당신의 이름을 입력하세요: ")

    print("\n가지고 있는 카드를 입력하세요. 쉼표(,)로 구분합니다.")
    print(f"카드 목록: {', '.join(ALL_CARDS)}")
    my_cards_str = input("내 카드: ")
    my_cards = [card.strip() for card in my_cards_str.split(',')]

    # 2. 게임 헬퍼 객체 생성
    game = ClueHelper(num_players, player_names, my_name, my_cards)
    print("\n초기 설정이 완료되었습니다. 게임을 시작하세요.")
    game.display_status()

    # 3. 메인 루프
    while True:
        print("\n[메뉴] 1: 추리 기록 | 2: 현황 보기 | 3: 다음 수 추천 | 4: 종료")
        choice = input("선택: ")

        if choice == '1':
            suggester = input("  - 추리한 사람: ")
            cards_str = input("  - 추리한 카드 3장 (쉼표로 구분): ")
            suggestion_cards = [c.strip() for c in cards_str.split(',')]

            shower = input("  - 카드를 보여준 사람 (없으면 그냥 Enter): ")
            if not shower:
                game.record_suggestion(suggester, suggestion_cards, None)
            else:
                if shower == my_name:
                    print("  - 당신이 카드를 보여줬으므로, 이 정보는 이미 알고 있습니다.")
                    continue

                shown_to_me = input(f"  - {shower}가 당신에게 카드를 보여줬나요? (y/n): ").lower()
                if shown_to_me == 'y':
                    shown_card = input("  - 보여준 카드는 무엇인가요?: ")
                    game.record_suggestion(suggester, suggestion_cards, shower, shown_card)
                else:
                    game.record_suggestion(suggester, suggestion_cards, shower)

            game.display_status()

        elif choice == '2':
            game.display_status()

        elif choice == '3':
            game.recommend_move()

        elif choice == '4':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 다시 선택해주세요.")


if __name__ == "__main__":
    main()