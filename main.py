from clue_logic import *
from clue_data import ALL_CARDS


def main():
    print("클루(Clue) 추리 보조 프로그램을 시작합니다.")

    num_players = int(input("총 플레이어 인원 수를 입력하세요: "))

    players = []
    for i in range(num_players):
        name = input(f"플레이어 {i + 1}의 이름을 입력하세요 (시계방향 순서): ")
        players.append(name)

    # player_names = [input(f"플레이어 {i + 1}의 이름을 입력하세요 (시계방향 순서): ") for i in range(num_players)]
    my_name = input("당신의 이름을 입력하세요: ")

    print("\n가지고 있는 카드를 입력하세요. 쉼표(,)로 구분합니다.")
    print(f"카드 목록: {', '.join(ALL_CARDS)}")
    my_cards = [card.strip() for card in input("내 카드: ").split(',')]

    game = ClueHelper(players, my_name, my_cards)
    print("\n초기 설정이 완료되었습니다. 게임을 시작하세요.")
    game.display_status()

    while True:
        print("\n[메뉴] 1: 추리 기록 | 2: 현황 보기 | 3: 다음 수 추천 | 4: 종료")
        choice = input("선택: ")

        if choice == '1':
            pass
            suggester = input("  - 추리한 사람: ")
            suggestion_cards = [c.strip() for c in input("  - 추리 카드 3장: ").split(',')]
            shower = input("  - 카드를 보여준 사람 (없으면 Enter): ")

            if suggester == my_name:
                # 추리한 카드 3장에 대해 각각 정답일 경우의 수 계산 (knowledge 기반)
                previous_cases = game.calculate_cases(suggestion_cards)

                game.process_my_suggestion(suggester, suggestion_cards, shower)

                # 확률 정규화 로직1 => 추리한 카드 3장에 대해 각각 (knowledge 기반)
                # 전체 후보리스트: players + envelope
                next_cases = game.calculate_cases(suggestion_cards)
                weight = previous_cases / next_cases

                # Normalize 진행
                suspects_left = [s for s in SUSPECTS if not game.knowledge[s]['owner']]
                weapons_left = [w for w in WEAPONS if not game.knowledge[w]['owner']]
                rooms_left = [r for r in ROOMS if not game.knowledge[r]['owner']]

                # left 카드 중 Suggestion 카드에 가중치: weight(45 line)
                # left 카드 중 Suggestion 아닌 카드에 가중치 1
                # Suggestion 중 shown 카드는 제외
                # 각 카드의 가중치 / 각 카드 가중치의 합 => updated probability

                # 제외할 플레이어들: 해당 카드

            else:
                pass
                # Process suggestion
                # 확률 정규화 로직2

            # if not shower:
            #     # 만약에 나도 카드를 안 들고 있고 나머지 플레이어들도 안 가지고 있으면 그 카드는 정답.
            #     pass
            # #     game.record_suggestion(suggester, suggestion_cards, None)
            # else:
            #     # 1. 추리한 플레이어와(suggester) 보여준 플레이어(shower) 사이에 있는 플레이어들은 추리한 카드 3장 모두 들고 있지 않다.
            #     # 2.
            #     pass
            #     if shower == my_name:
            #         print("  - 당신이 보여준 경우는 생략합니다.")
            #         continue
            #     shown_to_me = input(f"  - {shower}가 당신에게 카드를 보여줬나요? (y/n): ").lower()
            #     if shown_to_me == 'y':
            #         shown_card = input("  - 보여준 카드는 무엇인가요?: ")
            #         game.record_suggestion(suggester, suggestion_cards, shower, shown_card)
            #     else:
            #         game.record_suggestion(suggester, suggestion_cards, shower)
            # game.display_status()

        elif choice == '2':
            game.display_status()
        elif choice == '3':
            pass
            # game.recommend_move()
        elif choice == '4':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 다시 선택해주세요.")


if __name__ == "__main__":
    main()
