"""AgroSentry - AI Farm Assistant

Local sensor-based farm intelligence.
No external AI API is used.
"""

import streamlit as st

from utils.ai_agent import ai_reply
from utils.theme import inject_theme
from utils.auth import logout_button

inject_theme()

try:
    from utils.theme import topnav
except ImportError:
    topnav = None

if topnav:
    topnav("assistant")

st.title("🤖 AI Farm Assistant")
st.caption("Local farm intelligence powered by your AgroSentry sensor data.")
st.info("This assistant does not use ChatGPT, Claude, or any external AI API. Recommendations are generated from your latest sensor readings.")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

st.subheader("Ask about your farm")

suggested_questions = [
    "How is my farm?",
    "Do I need irrigation?",
    "What is my soil moisture?",
    "What is the temperature?",
    "What is the humidity?",
    "What should I do now?",
]

cols = st.columns(3)
for index, question in enumerate(suggested_questions):
    with cols[index % 3]:
        if st.button(question, key=f"suggested_{index}", use_container_width=True):
            st.session_state["pending_question"] = question

for message in st.session_state["chat_history"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

pending_question = st.session_state.pop("pending_question", None)
question = st.chat_input("Ask about your farm...")

if pending_question:
    question = pending_question

if question:
    st.session_state["chat_history"].append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    answer = ai_reply(question, history=st.session_state["chat_history"][:-1])
    st.session_state["chat_history"].append({"role": "assistant", "content": answer})

    with st.chat_message("assistant"):
        st.markdown(answer)
    st.rerun()

if st.session_state["chat_history"]:
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state["chat_history"] = []
        st.rerun()

st.caption("AgroSentry uses deterministic sensor rules and does not invent unavailable readings.")

try:
    logout_button()
except Exception:
    pass
