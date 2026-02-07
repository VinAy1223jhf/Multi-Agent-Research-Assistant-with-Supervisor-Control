# main.py
import streamlit as st
import uuid

from chatbot import run_task, get_conversation

# ----------------------------------
# Page Config
# ----------------------------------
st.set_page_config(
    page_title="🧠 Multi-Agent AI System",
    page_icon="🤖",
    layout="centered"
)

st.title("🧠 Multi-Agent AI System")
st.caption("Stateful multi-agent system powered by LangGraph")

# ----------------------------------
# Session: site_id = LangGraph thread
# ----------------------------------
if "site_id" not in st.session_state:
    st.session_state.site_id = str(uuid.uuid4())

if "clear_chat" not in st.session_state:
    st.session_state.clear_chat = False

site_id = st.session_state.site_id

# ----------------------------------
# Clear Chat Button (NO FULL RELOAD)
# ----------------------------------
col1, col2 = st.columns([6, 1])
with col2:
    if st.button("🧹 Clear"):
        st.session_state.site_id = str(uuid.uuid4())
        st.session_state.clear_chat = True
        st.toast("Chat cleared 🧹")

# ----------------------------------
# Display Chat History (LangGraph)
# ----------------------------------
if not st.session_state.clear_chat:
    chat_history = get_conversation(site_id)
else:
    chat_history = []

for msg in chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

st.session_state.clear_chat = False

# ----------------------------------
# User Input
# ----------------------------------
user_input = st.chat_input("Describe your task...")

if user_input:
    # Show user message immediately
    with st.chat_message("user"):
        st.markdown(user_input)

    # Run LangGraph workflow
    with st.chat_message("assistant"):
        with st.spinner("Supervisor coordinating agents... 🤔"):
            response = run_task(
                task=user_input,
                site_id=site_id
            )
            st.markdown(response)

    # Refresh UI from LangGraph memory (soft refresh)
    st.rerun()
