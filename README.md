# finance

파이썬 기초 문법을 배운 뒤, 분석, 시각화, 전처리, 머신러닝까지 진행한 뒤
`Streamlit`으로 간단한 웹 앱을 만들어 보는 실습 저장소입니다.

이 README는 아래 실습 파일들을 초보자가 직접 실행하고 코드를 읽어 볼 수 있도록 설명합니다.

## 파일 목록

| 구분 | 파일 | 한 줄 설명 |
| --- | --- | --- |
| Python 기초 | `day1-1-자료구조-제어문.ipynb` | 파이썬 주석, 변수, 자료구조, 조건문, 반복문을 연습하는 기초 문법 실습 노트북입니다. |
| 데이터 수집 | `day1-2-1-수집-JSON-API-호출(어려운_소스_참고용).ipynb` | 동행복권 JSON API로 로또 회차, 당첨번호, 보너스 번호를 수집하는 참고용 노트북입니다. |
| 데이터 수집 | `day1-2-2-selenium-BeautifulSoup.ipynb` | Selenium으로 로또 페이지 HTML을 가져오고 BeautifulSoup로 당첨번호를 파싱하는 웹 수집 실습 노트북입니다. |
| 분석/시각화 | `day1-3-분석-시각화.ipynb` | 타이타닉 데이터를 불러와 결측치, 통계, 그래프를 확인하는 데이터 분석과 시각화 실습 노트북입니다. |
| 전처리 | `day2-1-전처리.ipynb` | 타이타닉 데이터의 성별 변환, 결측치 처리 등 머신러닝 전 데이터 전처리를 실습하는 노트북입니다. |
| 머신러닝 | `day2-2-머신러닝.ipynb` | 전처리된 타이타닉 데이터로 생존 여부를 예측하는 의사결정나무 머신러닝 실습 노트북입니다. |
| 머신러닝 | `day3-1-신용카드-고객-부도-예측.ipynb` | 신용카드 고객 데이터를 이용해 부도 여부를 예측하는 분류 모델 실습 노트북입니다. |
| 머신러닝 | `day3-2-hynix.ipynb` | SK하이닉스 주가 데이터를 이용해 다음 영업일 종가를 선형회귀, Ridge, Lasso 모델로 예측해 보는 노트북입니다. |
| 테스트 | `test1.ipynb` | seaborn의 penguins 예제 데이터로 종별 변수 관계를 pairplot으로 시각화하는 간단한 테스트 노트북입니다. |
| Streamlit | `lotto.py` | 버튼을 누르면 합계 조건을 만족하는 로또 번호 5게임을 생성하는 가장 단순한 Streamlit 앱입니다. |
| Streamlit | `lotto2.py` | 로또 번호 생성 옵션, 통계, 기록, CSV 다운로드 기능을 포함한 확장형 Streamlit 앱입니다. |
| Streamlit | `stock.py` | 한국 주식 종목을 선택해 주가 데이터와 캔들스틱 차트를 보여주는 Streamlit 대시보드입니다. |
| Streamlit | `stock2.py` | 주가 조회, 이동평균선, 오류 처리 설명을 더 쉽게 정리한 초보자용 Streamlit 주식 대시보드입니다. |

## 1. 먼저 알아둘 것

Streamlit 앱 파일은 일반 파이썬 파일이지만, 실행은 `python 파일명.py`가 아니라 `streamlit run 파일명.py`로 합니다.

Streamlit은 파이썬 코드로 웹 화면을 쉽게 만드는 도구입니다. 실행하면 터미널에 주소가 나오고, 보통 브라우저가 자동으로 열립니다.

예:

```bash
streamlit run lotto.py
```

브라우저가 자동으로 열리지 않으면 터미널에 나오는 주소를 복사해서 브라우저에 붙여 넣으면 됩니다.

보통 이런 주소가 나옵니다.

```text
http://localhost:8501
```

## 2. 설치하기

로또 예제만 실행하려면 `streamlit`만 있으면 됩니다.

```bash
pip install streamlit
```

주식 예제까지 실행하려면 아래 패키지도 필요합니다.

```bash
pip install streamlit finance-datareader plotly pandas requests urllib3
```

## 3. 실행 순서 추천

처음 실습한다면 아래 순서로 보는 것을 추천합니다.

1. `lotto.py`
2. `lotto2.py`
3. `stock2.py`
4. `stock.py`

`lotto.py`가 가장 짧고, `lotto2.py`는 Streamlit 기능이 조금 더 많습니다.

주식 예제는 인터넷으로 데이터를 가져오므로 로또 예제보다 오류가 날 가능성이 높습니다. 그래서 코드 설명이 더 친절한 `stock2.py`를 먼저 보고, 그 다음 `stock.py`를 비교하는 순서가 좋습니다.

## 4. 실행 명령 모음

```bash
streamlit run lotto.py
streamlit run lotto2.py
streamlit run stock2.py
streamlit run stock.py
```
