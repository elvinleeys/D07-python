import json
import os
import urllib.parse
import urllib.request

import streamlit as st

# 같은 폴더의 .env 에서 KEY=값 줄을 읽어 환경변수로 등록 (이미 설정된 값이 우선)
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.exists(env_path):
    with open(env_path, encoding="utf-8") as f:
        for line in f:
            key, sep, value = line.strip().partition("=")
            if sep and not key.startswith("#"):
                os.environ.setdefault(key.strip(), value.strip())

st.title("서울 현재 날씨")

API_KEY = os.environ.get("OPENWEATHER_API_KEY")
if not API_KEY:
    st.error("환경변수 OPENWEATHER_API_KEY 가 설정되지 않았습니다.")
    st.stop()

query = urllib.parse.urlencode(
    {"q": "Seoul", "appid": API_KEY, "units": "metric", "lang": "kr"}
)
try:
    with urllib.request.urlopen(f"https://api.openweathermap.org/data/2.5/weather?{query}", timeout=10) as res:
        data = json.load(res)
except Exception as e:
    st.error(f"날씨 정보를 가져오지 못했습니다: {e}")
    st.stop()

st.subheader(data["weather"][0]["description"])
c1, c2, c3 = st.columns(3)
c1.metric("기온", f"{data['main']['temp']}°C")
c2.metric("체감 온도", f"{data['main']['feels_like']}°C")
c3.metric("습도", f"{data['main']['humidity']}%")
st.button("새로고침")
