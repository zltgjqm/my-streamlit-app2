import streamlit as st
from openai import OpenAI

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="My AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# -----------------------------
# 커스텀 CSS
# -----------------------------
st.markdown("""
<style>
.chat-title {
    font-size: 2.2rem;
    font-weight: 700;
    background: linear-gradient(90deg, #6a5af9, #f857a6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.3em;
}
.chat-subtitle {
    color: #888;
    margin-bottom: 1.5em;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 타이틀
# -----------------------------
st.markdown('<div class="chat-title">🤖 나의 AI 챗봇</div>', unsafe_allow_html=True)
st.markdown('<div class="chat-subtitle">간단하고 깔끔한 대화형 AI</div>', unsafe_allow_html=True)

# -----------------------------
# 사이드바
# -----------------------------
with st.sidebar:
    st.header("⚙️ 설정")
    api_key = st.text_input("OpenAI API Key", type="password")
    st.caption("API 키는 저장되지 않습니다.")

# -----------------------------
# 대화 기록 초기화
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# 이전 대화 표시
# -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# 사용자 입력
# -----------------------------
if prompt := st.chat_input("메시지를 입력하세요..."):
    if not api_key:
        st.error("⚠️ 사이드바에서 API Key를 입력해주세요!")
    else:
        # 사용자 메시지
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI 응답
        with st.chat_message("assistant"):
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
            st.markdown(reply)

            st.session_state.messages.append({
                "role": "assistant",
                "content": reply
            })
