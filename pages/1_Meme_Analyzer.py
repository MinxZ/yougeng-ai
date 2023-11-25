import asyncio
from urllib.error import URLError

import altair as alt
import pandas as pd

import streamlit as st
from streamlit.hello.utils import show_code

from roles.meme_analyzer import MemeAnalyzer
from metagpt.logs import logger


DEFAULT_INPUT = "找点热梗！"
SEARCH_PROMPT = "搜些新梗！"

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

    if st.button(SEARCH_PROMPT):
        prompt = SEARCH_PROMPT

    if prompt:
        st.chat_message("user").write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            role = MemeAnalyzer()
            logger.info(prompt)
            profile = f"{role._setting.name} ({role.profile})"
            result = asyncio.run(role.run(prompt))
            output_string = str(result.content)
            output_string = output_string.replace("Meme Analyzer: ", "")
            st.markdown(f"**{profile}:** \n\n{output_string}")
            logger.info(result.content)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": result})


st.set_page_config(page_title="热梗分析师 Meme Analyzer", page_icon="🤣")
st.markdown("# 🤣 热梗分析师 Meme Analyzer")
st.sidebar.header("🤣 热梗分析师 Meme Analyzer")

run_role()
