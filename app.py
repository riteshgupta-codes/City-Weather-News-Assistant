import os
import sys
from pathlib import Path

# Force the directory containing agent.py to be at the very top of sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import streamlit as st
from agent import run_agent

st.set_page_config(page_title="City Assistant", page_icon="🤖")

st.title("🤖 City Weather & News Assistant")

# ==============================
# SESSION STATE
# ==============================
if "chat" not in st.session_state:
    st.session_state.chat = []

# Show chat
for role, msg in st.session_state.chat:
    with st.chat_message(role):
        st.write(msg)

# ==============================
# USER INPUT
# ==============================
user_input = st.chat_input("Ask something...")

if user_input:
    # Show user
    st.chat_message("user").write(user_input)
    st.session_state.chat.append(("user", user_input))

    # Assistant
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                answer = run_agent(user_input)
                st.write(answer)
                st.session_state.chat.append(("assistant", answer))
            except Exception as e:
                st.error(str(e))