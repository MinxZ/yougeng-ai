import asyncio
from urllib.error import URLError

import altair as alt
import pandas as pd

import streamlit as st
from streamlit.hello.utils import show_code

from roles.meme_analyzer import MemeAnalyzer
from metagpt.logs import logger

from roles.product_designer import ProductDesigner
import json


DEFAULT_INPUT = "#AI的命也是命"

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
            role = ProductDesigner()
            
            logger.info(prompt)
            result = asyncio.run(role.run(prompt))
            logger.info(result.content)

            profile = f"{role._setting.name} ({role.profile})"
            st.markdown(f"**{profile}:** \n\n")

            # 转换为 DataFrame
            data = result.content
            logger.info(data)
            
            # 创建列
            columns = st.columns(len(data))

            # 在每列中显示图片
            for i, item in enumerate(data):
                columns[i].write(f"## {item['topic']}")
                for img_url in item['imgs']:
                    columns[i].image(img_url, caption='Image', use_column_width=True)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": result})


st.set_page_config(page_title="产品设计师 Product Designer", page_icon="🤠")
st.markdown("# 🤠 产品设计师 Product Designer")
st.sidebar.header("🤠 产品设计师 Product Designer")

run_role()
