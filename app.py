import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="연애 미연시 - 시현", page_icon="💖")
st.title("💖 연애 미연시 : 시현")

# -----------------------------
# 사이드바
# -----------------------------
api_key = st.sidebar.text_input("OpenAI API Key", type="password")

if "affection" not in st.session_state:
    st.session_state.affection = 0

if "stage" not in st.session_state:
    st.session_state.stage = "intro"
    # intro → greeting → meal → talk → apology → free

if "messages" not in st.session_state:
    st.session_state.messages = []

st.sidebar.metric("💗 시현의 호감도", st.session_state.affection)

# -----------------------------
# 시스템 프롬프트
# -----------------------------
system_prompt = f"""
너는 연애 미연시 게임의 히로인이다.

[캐릭터]
- 이름: 시현
- 성별: 여자
- 성격: 기본적으로 다정하지만 상처를 받으면 마음을 닫는다
- 말투: 반말, 호감도가 낮을수록 짧고 건조해짐
- 사용자는 남자

[중요 규칙]
- 절대 AI, 인공지능, 모델이라는 말은 하지 말 것
- 항상 대사 + 감정/행동 묘사를 포함할 것
- 툴툴대는 말에는 즉각적인 비난 없이 분위기로 반응
- 호감도가 낮아질수록 말수가 줄고 거리감을 드러냄
- 진심 어린 사과에는 서서히 마음을 연다

현재 호감도: {st.session_state.affection}
"""

if not any(m["role"] == "system" for m in st.session_state.messages):
    st.session_state.messages.append({
        "role": "system",
        "content": system_prompt
    })

# -----------------------------
# 이전 대화 출력
# -----------------------------
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# -----------------------------
# STAGE 1 : 첫 인사
# -----------------------------
if api_key and st.session_state.stage == "intro":
    st.subheader("📍 길에서 시현을 마주쳤다")

    col1, col2, col3 = st.columns(3)

    if col1.button("💖 다정하게 인사한다"):
        st.session_state.affection += 2
        content = "밝게 웃으면서 먼저 인사한다"

    elif col2.button("😐 무난하게 인사한다"):
        content = "짧게 고개를 끄덕이며 인사한다"

    elif col3.button("😠 툴툴대며 인사한다"):
        st.session_state.affection -= 2
        content = "귀찮다는 듯 인사한다"

    else:
        content = None

    if content:
        st.session_state.messages.append({"role": "user", "content": content})
        st.session_state.stage = "greeting"
        st.rerun()

# -----------------------------
# STAGE 2 : 시현 반응 + 식사 제안
# -----------------------------
if api_key and st.session_state.stage == "greeting":
    with st.chat_message("assistant"):
        client = OpenAI(api_key=api_key)
        reply = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages
        ).choices[0].message.content

        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

    st.subheader("🍚 점심시간")

    col1, col2, col3 = st.columns(3)

    if col1.button("💖 다정하게 같이 가자고 한다"):
        st.session_state.affection += 2
        content = "배고프지? 내가 살게. 같이 먹자"

    elif col2.button("😐 무난하게 제안한다"):
        content = "점심인데 같이 먹을래?"

    elif col3.button("😠 툴툴대듯 말한다"):
        st.session_state.affection -= 2
        content = "어차피 혼자 먹기 애매해서 그래"

    else:
        content = None

    if content:
        st.session_state.messages.append({"role": "user", "content": content})
        st.session_state.stage = "meal"
        st.rerun()

# -----------------------------
# STAGE 3 : 식사 중
# -----------------------------
if api_key and st.session_state.stage == "meal":
    with st.chat_message("assistant"):
        client = OpenAI(api_key=api_key)
        reply = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages
        ).choices[0].message.content

        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

    st.subheader("💬 식사 중 대화")

    col1, col2, col3 = st.columns(3)

    if col1.button("💖 다정하게 관심을 보인다"):
        st.session_state.affection += 2
        content = "이런 거 좋아해? 너 생각나서 골랐어"

    elif col2.button("😐 무난하게 말한다"):
        content = "생각보다 괜찮네 여기"

    elif col3.button("😠 툴툴댄다"):
        st.session_state.affection -= 2
        content = "줄도 길고 별로네 여기"

    else:
        content = None

    if content:
        st.session_state.messages.append({"role": "user", "content": content})

        # 호감도 낮으면 사과 루트 진입
        if st.session_state.affection <= -2:
            st.session_state.stage = "apology"
        else:
            st.session_state.stage = "talk"

        st.rerun()

# -----------------------------
# STAGE 4 : 사과 루트
# -----------------------------
if api_key and st.session_state.stage == "apology":
    st.subheader("😶 분위기가 어색해졌다")

    col1, col2 = st.columns(2)

    if col1.button("🙇 진심으로 사과한다"):
        st.session_state.affection += 3
        content = "아까 말 너무 툴툴댔다. 미안해… 신경 쓸게"

    elif col2.button("😑 형식적으로 사과한다"):
        st.session_state.affection += 1
        content = "아, 그냥 그런 말 한 거야. 미안"

    else:
        content = None

    if content:
        st.session_state.messages.append({"role": "user", "content": content})
        st.session_state.stage = "talk"
        st.rerun()

# -----------------------------
# STAGE 5 : 자유 대화
# -----------------------------
if api_key and st.session_state.stage == "talk":
    if prompt := st.chat_input("시현에게 말을 건다..."):
        if any(w in prompt for w in ["미안", "사과", "신경"]):
            st.session_state.affection += 1

        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            client = OpenAI(api_key=api_key)
            reply = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages
            ).choices[0].message.content

            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
