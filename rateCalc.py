import json
import os
import urllib.request
from email.utils import parsedate_to_datetime
from zoneinfo import ZoneInfo

import streamlit as st

API = {
    "환율": "https://v6.exchangerate-api.com/v6/{key}/latest/{base}",  # 🔌
}

# 같은 폴더의 .env 에서 KEY=값 줄을 읽어 환경변수로 등록 (이미 설정된 값이 우선)
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.exists(env_path):
    with open(env_path, encoding="utf-8") as f:
        for line in f:
            key, sep, value = line.strip().partition("=")
            if sep and not key.startswith("#"):
                os.environ.setdefault(key.strip(), value.strip())

CURRENCIES = ["KRW", "USD", "EUR", "JPY", "CNY", "GBP", "AUD", "CAD"]
COLORS = ["#FF6B6B", "#FF9F43", "#FECA57", "#1DD1A1", "#48DBFB", "#54A0FF", "#5F27CD", "#F368E0"]

st.markdown(
    "<h1 style='background:linear-gradient(90deg,#FF6B6B,#FECA57,#1DD1A1,#54A0FF,#F368E0);"
    "-webkit-background-clip:text;color:transparent'>💱 환율 계산기</h1>",
    unsafe_allow_html=True,
)

API_KEY = os.getenv("EXCHANGERATE_API_KEY")
if not API_KEY:
    st.error("환경변수 EXCHANGERATE_API_KEY 가 설정되지 않았습니다.")
    st.stop()

c1, c2, c3 = st.columns([2, 1, 1])
amount = c1.number_input("금액", min_value=0.0, value=1.0, step=1.0)
base = c2.selectbox("기준 통화", CURRENCIES, index=1)
target = c3.selectbox("대상 통화", CURRENCIES, index=0)

try:
    url = API["환율"].format(key=API_KEY, base=base)
    with urllib.request.urlopen(url, timeout=10) as res:
        data = json.load(res)
    if data["result"] != "success":
        raise ValueError
except Exception:
    # 예외 메시지에 주소(키 포함)가 섞일 수 있어 출력하지 않는다
    st.error("환율 정보를 가져오지 못했습니다. API 키와 네트워크를 확인하세요.")
    st.stop()

rates = data["conversion_rates"]
st.markdown(
    f"<div style='padding:20px;border-radius:14px;color:white;font-size:1.6rem;font-weight:700;"
    f"background:linear-gradient(135deg,#5F27CD,#F368E0)'>"
    f"{amount:,.2f} {base} = {amount * rates[target]:,.2f} {target}</div>",
    unsafe_allow_html=True,
)

st.subheader(f"1 {base} 기준 환율")
for col, cur, color in zip(st.columns(len(CURRENCIES)), CURRENCIES, COLORS):
    col.markdown(
        f"<div style='background:{color};border-radius:10px;padding:8px;text-align:center;color:white'>"
        f"<b>{cur}</b><br>{rates[cur]:,.4f}</div>",
        unsafe_allow_html=True,
    )

updated = parsedate_to_datetime(data["time_last_update_utc"]).astimezone(ZoneInfo("Asia/Seoul"))
st.caption(f"기준 시각: {updated:%Y-%m-%d %H:%M} (한국 시간) · 무료 플랜은 하루 1회 갱신됩니다.")
