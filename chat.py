import json
import os
import urllib.request

import streamlit as st

API = {
    "채팅": "https://api.openai.com/v1/chat/completions",  # 🔌
}
MODEL = "gpt-4o-mini"

# 같은 폴더의 .env 에서 KEY=값 줄을 읽어 환경변수로 등록 (이미 설정된 값이 우선)
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.exists(env_path):
    with open(env_path, encoding="utf-8") as f:
        for line in f:
            key, sep, value = line.strip().partition("=")
            if sep and not key.startswith("#"):
                os.environ.setdefault(key.strip(), value.strip())

st.title("🤖 챗봇")

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    st.error("환경변수 OPENAI_API_KEY 가 설정되지 않았습니다.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

if prompt := st.chat_input("메시지를 입력하세요"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    req = urllib.request.Request(
        API["채팅"],
        data=json.dumps({"model": MODEL, "messages": st.session_state.messages}).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as res:
            reply = json.load(res)["choices"][0]["message"]["content"]
    except Exception:
        # 예외 메시지에 요청 정보가 섞일 수 있어 출력하지 않는다
        st.session_state.messages.pop()
        st.error("답변을 가져오지 못했습니다. API 키와 네트워크를 확인하세요.")
        st.stop()

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
