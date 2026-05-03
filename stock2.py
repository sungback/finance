# 설치:
#   pip install -r requirements.txt
#
# 실행:
#   streamlit run stock2.py

from datetime import datetime, timedelta

# FinanceDataReader는 주가 데이터, plotly는 차트, streamlit은 웹 화면을 담당합니다.
import FinanceDataReader as fdr
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(page_title="주가 정보 분석 대시보드", layout="wide")
st.title("주가 정보 분석 대시보드")


@st.cache_data
def get_stock_list():
    # fdr.StockListing("KRX")는 코스피/코스닥 종목 목록을 DataFrame으로 돌려줍니다.
    stock_list = fdr.StockListing("KRX")
    # 종목명(Name)과 종목코드(Code)만 사용하고, 비어 있는 행은 제거합니다.
    stock_list = stock_list[["Name", "Code"]].dropna()
    # 종목코드는 005930처럼 앞의 0이 중요하므로 문자열 6자리로 맞춥니다.
    stock_list["Code"] = stock_list["Code"].astype(str).str.zfill(6)
    # 예: "삼성전자 (005930)" 형태로 만들면 검색과 코드 추출이 쉬워집니다.
    return (stock_list["Name"] + " (" + stock_list["Code"] + ")").tolist()


@st.cache_data(ttl=3600)
def get_stock_data(code, start_date, end_date):
    try:
        # FinanceDataReader는 날짜를 "YYYY-MM-DD" 형태의 문자열로 받으면 이해하기 쉽습니다.
        start_text = start_date.strftime("%Y-%m-%d")
        end_text = end_date.strftime("%Y-%m-%d")
        return fdr.DataReader(code, start_text, end_text)
    except Exception as error:
        # 인터넷 연결, 종목 코드, 날짜 범위 등에 문제가 있으면 화면에 오류를 보여줍니다.
        st.error(f"주가 데이터를 불러오지 못했습니다: {error}")
        return None


def get_ticker_code(stock_name):
    # "삼성전자 (005930)"에서 "005930"만 꺼냅니다.
    return stock_name.split("(")[-1].replace(")", "").strip()


st.sidebar.header("조회 설정")

try:
    options = get_stock_list()
except Exception as error:
    st.error(f"종목 목록을 불러오지 못했습니다: {error}")
    st.stop()

# selectbox는 드롭다운 목록이며, 글자를 입력해서 검색할 수도 있습니다.
target_stock = st.sidebar.selectbox(
    "종목 선택",
    options=options,
    index=None,
    placeholder="종목명 또는 코드를 입력하세요",
)

today = datetime.now().date()
default_start = today - timedelta(days=365)

start_date = st.sidebar.date_input("시작일", default_start)
end_date = st.sidebar.date_input("종료일", today)
show_moving_average = st.sidebar.checkbox("20일 이동평균선 표시", value=True)

# 아직 종목을 선택하지 않았다면 안내 문구만 보여주고 여기서 멈춥니다.
if not target_stock:
    st.info("왼쪽 사이드바에서 종목을 선택해 주세요.")
    st.stop()

# 시작일이 종료일보다 늦으면 데이터를 조회할 수 없으므로 먼저 검사합니다.
if start_date > end_date:
    st.warning("시작일은 종료일보다 늦을 수 없습니다.")
    st.stop()

ticker_code = get_ticker_code(target_stock)

with st.spinner(f"{target_stock} 데이터를 가져오는 중입니다."):
    df = get_stock_data(ticker_code, start_date, end_date)

# 데이터가 없으면 이후 계산과 차트에서 오류가 나므로 여기서 멈춥니다.
if df is None or df.empty:
    st.warning("조회된 데이터가 없습니다. 종목 코드나 날짜를 확인해 주세요.")
    st.stop()

# 날짜 순서가 오래된 날짜에서 최신 날짜로 정렬되도록 맞춥니다.
df = df.sort_index()

if show_moving_average:
    # rolling(window=20)은 최근 20개 거래일의 평균을 계산합니다.
    df["MA20"] = df["Close"].rolling(window=20, min_periods=1).mean()

# iloc[-1]은 DataFrame의 마지막 행, 즉 가장 최근 거래일 데이터를 의미합니다.
last_price = df["Close"].iloc[-1]

# 전일 대비 가격 변화는 최근 종가와 바로 전 거래일 종가의 차이입니다.
if len(df) >= 2:
    prev_price = df["Close"].iloc[-2]
    price_change = last_price - prev_price
else:
    price_change = None
    st.info("조회된 거래일이 1일뿐이라 전일 대비 변화량은 표시하지 않습니다.")

col1, col2, col3, col4 = st.columns(4)

if price_change is None:
    col1.metric("현재가", f"{last_price:,.0f} 원")
else:
    col1.metric("현재가", f"{last_price:,.0f} 원", f"{price_change:,.0f} 원")

col2.metric("고가", f"{df['High'].iloc[-1]:,.0f} 원")
col3.metric("저가", f"{df['Low'].iloc[-1]:,.0f} 원")
col4.metric("거래량", f"{df['Volume'].iloc[-1]:,.0f}")

# tabs를 사용하면 한 화면에서 여러 차트를 나누어 볼 수 있습니다.
tab1, tab2 = st.tabs(["캔들스틱 차트", "종가 라인 차트"])

with tab1:
    fig = go.Figure()

    # 캔들스틱 차트는 시가(Open), 고가(High), 저가(Low), 종가(Close)를 함께 보여줍니다.
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name=target_stock,
        )
    )

    if show_moving_average:
        # 이동평균선은 캔들 차트 위에 선 그래프로 추가합니다.
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["MA20"],
                mode="lines",
                name="20일 이동평균",
            )
        )

    fig.update_layout(
        template="plotly_white",
        height=600,
        margin=dict(l=20, r=20, t=20, b=20),
    )
    fig.update_xaxes(rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    if show_moving_average:
        st.line_chart(df[["Close", "MA20"]])
    else:
        st.line_chart(df["Close"])

# expander는 접었다 펼 수 있는 영역입니다. 원본 데이터를 확인할 때 유용합니다.
with st.expander("Raw Data 보기"):
    st.dataframe(df.sort_index(ascending=False), use_container_width=True)

# 화면 맨 아래에 데이터 출처와 마지막 실행 시간을 표시합니다.
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Data by FinanceDataReader")
