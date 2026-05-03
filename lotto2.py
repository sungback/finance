# 설치:
#   pip install -r requirements.txt
#
# 실행:
#   streamlit run lotto2.py

import csv
import random
from datetime import datetime
from io import StringIO

import streamlit as st


st.set_page_config(page_title="로또 번호 생성기", layout="wide")
st.title("로또 번호 생성기")
st.markdown("Streamlit의 여러 입력/출력 기능을 연습하는 예제입니다.")


def generate_one_game(sort_numbers=True):
    # 1부터 45까지 숫자 중에서 서로 다른 숫자 6개를 뽑습니다.
    numbers = random.sample(range(1, 46), 6)

    if sort_numbers:
        numbers = sorted(numbers)

    return numbers


def check_strategy(numbers, use_high_sum, use_big_numbers, avoid_sequence, balance_odd_even):
    total = sum(numbers)

    # 생일 번호(1~31) 위주 조합을 피하기 위해 합계가 높은 조합을 사용합니다.
    if use_high_sum and not 170 <= total <= 210:
        return False

    # 32 이상 숫자가 2개 이상 들어가도록 합니다.
    big_number_count = len([number for number in numbers if number >= 32])
    if use_big_numbers and big_number_count < 2:
        return False

    # 3개 이상 연속되는 숫자 조합은 피합니다.
    if avoid_sequence:
        sorted_numbers = sorted(numbers)
        sequence_count = 1

        for index in range(1, len(sorted_numbers)):
            if sorted_numbers[index] == sorted_numbers[index - 1] + 1:
                sequence_count = sequence_count + 1
            else:
                sequence_count = 1

            if sequence_count >= 3:
                return False

    # 홀수와 짝수가 너무 한쪽으로 몰리지 않게 합니다.
    odd_count = len([number for number in numbers if number % 2 == 1])
    if balance_odd_even and not 2 <= odd_count <= 4:
        return False

    return True


def make_games(game_count, sort_numbers, use_high_sum, use_big_numbers, avoid_sequence, balance_odd_even):
    games = []
    failed_count = 0
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for game_number in range(1, game_count + 1):
        selected_numbers = None

        # 조건을 너무 많이 켰을 때 무한 반복하지 않도록 최대 1000번까지만 시도합니다.
        for _ in range(1000):
            numbers = generate_one_game(sort_numbers)

            if check_strategy(numbers, use_high_sum, use_big_numbers, avoid_sequence, balance_odd_even):
                selected_numbers = numbers
                break

        if selected_numbers is None:
            failed_count = failed_count + 1
            continue

        odd_count = len([number for number in selected_numbers if number % 2 == 1])
        big_number_count = len([number for number in selected_numbers if number >= 32])

        games.append(
            {
                "생성시각": created_at,
                "게임": game_number,
                "번호": " ".join([str(number) for number in selected_numbers]),
                "합계": sum(selected_numbers),
                "홀수": odd_count,
                "32이상": big_number_count,
            }
        )

    return games, failed_count


def make_csv(games):
    # download_button에 넘길 CSV 문자열을 만듭니다.
    output = StringIO()
    columns = ["생성시각", "게임", "번호", "합계", "홀수", "32이상"]
    writer = csv.DictWriter(output, fieldnames=columns)
    writer.writeheader()
    writer.writerows(games)
    return output.getvalue()


if "latest_games" not in st.session_state:
    st.session_state.latest_games = []

if "history" not in st.session_state:
    st.session_state.history = []


st.sidebar.header("생성 옵션")

game_count = st.sidebar.slider("생성할 게임 수", min_value=1, max_value=5, value=5)
sort_text = st.sidebar.radio("번호 표시 방식", ["오름차순 정렬", "뽑힌 순서 그대로"])
sort_numbers = sort_text == "오름차순 정렬"

st.sidebar.subheader("번호 선택 전략")
use_high_sum = st.sidebar.checkbox("합계 170~210 사용", value=True)
use_big_numbers = st.sidebar.checkbox("32 이상 숫자 2개 이상 포함", value=True)
avoid_sequence = st.sidebar.checkbox("3개 이상 연속 번호 피하기", value=True)
balance_odd_even = st.sidebar.checkbox("홀수 개수 2~4개로 맞추기", value=True)

col1, col2 = st.columns(2)
with col1:
    generate_button = st.button("로또 번호 생성")
with col2:
    reset_button = st.button("기록 초기화")

if reset_button:
    st.session_state.latest_games = []
    st.session_state.history = []
    st.success("생성 기록을 초기화했습니다.")

if generate_button:
    games, failed_count = make_games(
        game_count,
        sort_numbers,
        use_high_sum,
        use_big_numbers,
        avoid_sequence,
        balance_odd_even,
    )

    st.session_state.latest_games = games
    st.session_state.history.extend(games)

    if failed_count > 0:
        st.warning(f"{failed_count}개 게임은 조건이 너무 까다로워 만들지 못했습니다.")


with st.expander("번호 전략 설명"):
    st.markdown(
        """
        이 전략들은 당첨 확률을 높이는 방법이 아닙니다.
        로또의 모든 번호 조합은 같은 확률로 추첨됩니다.

        다만 사람들이 생일 번호처럼 1~31 사이 숫자를 많이 고른다고 가정하면,
        큰 숫자나 합계가 높은 조합은 다른 사람과 번호가 겹칠 가능성을 줄이는 데 도움이 될 수 있습니다.
        즉, 운 좋게 당첨됐을 때 상금을 나눌 가능성을 줄이는 전략으로 이해하면 됩니다.
        """
    )


tab1, tab2, tab3 = st.tabs(["번호 보기", "통계 보기", "기록 보기"])

with tab1:
    latest_games = st.session_state.latest_games

    if not latest_games:
        st.info("버튼을 눌러 로또 번호를 생성해 주세요.")
    else:
        game_columns = st.columns(5)

        for index, game in enumerate(latest_games):
            with game_columns[index % 5]:
                st.markdown(f"**{game['게임']}게임**")
                st.markdown(f"#### :green[{game['번호']}]")
                st.caption(f"합계 {game['합계']} | 홀수 {game['홀수']} | 32+ {game['32이상']}")

with tab2:
    latest_games = st.session_state.latest_games

    if not latest_games:
        st.info("통계를 보려면 먼저 번호를 생성해 주세요.")
    else:
        total_sum = sum([game["합계"] for game in latest_games])
        average_sum = total_sum / len(latest_games)
        average_big_number = sum([game["32이상"] for game in latest_games]) / len(latest_games)

        metric1, metric2, metric3 = st.columns(3)
        with metric1:
            st.metric("생성 게임 수", len(latest_games))
        with metric2:
            st.metric("평균 합계", f"{average_sum:.1f}")
        with metric3:
            st.metric("평균 32 이상 개수", f"{average_big_number:.1f}")

        st.subheader("게임별 합계")
        st.bar_chart({"합계": [game["합계"] for game in latest_games]})

with tab3:
    if not st.session_state.history:
        st.info("아직 저장된 생성 기록이 없습니다.")
    else:
        st.dataframe(st.session_state.history, use_container_width=True)

        csv_data = make_csv(st.session_state.history)
        st.download_button(
            "CSV 파일 다운로드",
            data=csv_data,
            file_name="lotto_history.csv",
            mime="text/csv",
        )
