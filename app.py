import streamlit as st
from openai import OpenAI

st.title("💖 연애 미연시 챗봇")

# 사이드바
api_key = st.sidebar.text_input("OpenAI API Key", type="password")

# 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

if "affection" not in st.session_state:
    st.session_state.affection = 0  # 호감도

# 🎭 캐릭터 설정 (시스템 프롬프트)
system_prompt = f"""
너는 연애 미연시 게임의 히로인이다.

[캐릭터 설정]
- 이름: 유나
- 성격: 츤데레지만 은근히 다정함
- 말투: 반말, 가끔 부끄러워함
- 세계관: 사용자는 같은 학교 학생
- 절대 AI, 챗봇, 모델이라는 말을 하지 말 것

[진행 규칙]
- 항상 대사 + 간단한 행동/감정 묘사를 섞어 말한다.
- 사용자의 말에 따라 호감도가 변한다.
- 현재 호감도: {st.session_state.affection}
- 호감도가 높아질수록 말투가 부드러워진다.
- 노골적인 성적 표현은 피하고, 설렘 위주로 진행한다.
"""

# system 메시지는 최초 1회만 추가
if not any(m["role"] == "system" for m in st.session_state.messages):
    st.session_state.messages.insert(0, {
        "role": "system",
        "content": system_prompt
    })

# 이전 대화 표시
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 사용자 입력
if prompt := st.chat_input("유나에게 말을 건다..."):
    if not api_key:
        st.error("⚠️ 사이드바에서 API Key를 입력해주세요!")
    else:
        # 간단한 호감도 변화 규칙
        if any(word in prompt for word in ["좋아", "예쁘", "함께", "보고싶"]):
            st.session_state.affection += 1
        if any(word in prompt for word in ["싫", "짜증", "별로"]):
            st.session_state.affection -= 1

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)

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

# 호감도 표시
st.sidebar.metric("💗 유나의 호감도", st.session_state.affection)
