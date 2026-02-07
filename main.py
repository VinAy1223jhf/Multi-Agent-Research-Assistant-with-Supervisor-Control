# main.py
import streamlit as st
import uuid

from chatbot import run_task, get_conversation

st.set_page_config(
    page_title="🧠 Multi-Agent AI System",
    page_icon="🤖",
    layout="centered"
)

st.title("🧠 Multi-Agent AI System")
st.caption("Stateful multi-agent system powered by LangGraph")

# ----------------------------------
# Site/User ID (stable per session)
# ----------------------------------
if "site_id" not in st.session_state:
    st.session_state.site_id = str(uuid.uuid4())

site_id = st.session_state.site_id

# ----------------------------------
# Fetch conversation from LangGraph
# ----------------------------------
chat_history = get_conversation(site_id)

for msg in chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ----------------------------------
# User input
# ----------------------------------
user_input = st.chat_input("Describe your task...")

if user_input:
    # Show user message immediately
    with st.chat_message("user"):
        st.markdown(user_input)

    # Run agent with LangGraph memory
    with st.chat_message("assistant"):
        with st.spinner("Supervisor coordinating agents... 🤔"):
            response = run_task(
                task=user_input,
                site_id=site_id
            )
            st.markdown(response)
    print("Task completed. Response:", response)
    st.rerun()  # 🔁 refresh UI from LangGraph memory
