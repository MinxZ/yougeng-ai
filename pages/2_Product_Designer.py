import asyncio
from urllib.error import URLError

import altair as alt
import pandas as pd

import streamlit as st
from streamlit.hello.utils import show_code

from roles.meme_analyzer import MemeAnalyzer
from metagpt.logs import logger


DEFAULT_INPUT = "#AgentLivesMatter"

def run_role():
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input(placeholder=DEFAULT_INPUT)
    
    if st.button(DEFAULT_INPUT):
        prompt = DEFAULT_INPUT

    if prompt:
        st.chat_message("user").write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            role = MemeAnalyzer()
            logger.info(prompt)
            profile = f"{role._setting.name} ({role.profile})"
            result = asyncio.run(role.run(prompt))
            st.markdown(f"**{profile}:** \n\n{result.content}")
            logger.info(result.content[:100])

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": result})


st.set_page_config(page_title="梗衣设计师 Cloth Designer", page_icon="🤠")
st.markdown("# 🤠 梗衣设计师 Cloth Designer")
st.sidebar.header("🤠 梗衣设计师 Cloth Designer")

run_role()
