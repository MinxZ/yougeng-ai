# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger

import os
from langchain.agents import ConversationalChatAgent, AgentExecutor
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import AzureChatOpenAI
from langchain.memory import ConversationBufferMemory, ChatMessageHistory
# from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.tools import DuckDuckGoSearchRun
import streamlit as st
import asyncio
from metagpt.roles.product_manager import ProductManager
from metagpt.logs import logger


LOGGER = get_logger(__name__)

# model
def get_chat_model():
    BASE_URL = "https://autoagents-ca-east.openai.azure.com/"
    API_KEY = "2864ce19a46540b2a0943df607ca6225"

    model = AzureChatOpenAI(
        temperature=0.5,
        openai_api_base=BASE_URL,
        openai_api_version="2023-08-01-preview",
        deployment_name="gpt-4",
        openai_api_key=API_KEY,
        openai_api_type="azure",
        streaming=True
    )
    return model

def run():
    # start
    st.set_page_config(page_title="有梗.ai", page_icon="😏")
    st.title("😏 有梗.ai Team")

    st.sidebar.success("Select a demo above.")

    # # history
    # msgs = ChatMessageHistory()
    # memory = ConversationBufferMemory(
    #     chat_memory=msgs, return_messages=True, memory_key="chat_history", output_key="output"
    # )
    # if len(msgs.messages) == 0: # or st.sidebar.button("Reset chat history"):
    #     msgs.clear()
    #     msgs.add_ai_message("How can I help you?")
    #     st.session_state.steps = {}

    # agent running
    if prompt := st.chat_input(placeholder="有梗，启动！"):
        st.chat_message("user").write(prompt)

        with st.chat_message("assistant"):
            msg = "Write a PRD for a snake game"
            role = ProductManager()
            result = asyncio.run(role.run(msg))
            st.write(result)
            # logger.info(result.content[:100])
        
        # llm = get_chat_model()
        # tools = [DuckDuckGoSearchRun(name="Search")]
        # chat_agent = ConversationalChatAgent.from_llm_and_tools(llm=llm, tools=tools)
        # executor = AgentExecutor.from_agent_and_tools(
        #     agent=chat_agent,
        #     tools=tools,
        #     memory=memory,
        #     return_intermediate_steps=True,
        #     handle_parsing_errors=True,
        # )
        # with st.chat_message("assistant"):
        #     st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        #     response = executor(prompt, callbacks=[st_cb])
        #     st.write(response["output"])
        #     st.session_state.steps[str(len(msgs.messages) - 1)] = response["intermediate_steps"]

if __name__ == "__main__":
    run()
