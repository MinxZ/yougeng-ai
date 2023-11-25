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
from roles.coder import SimpleCoder

LOGGER = get_logger(__name__)

def run():
    # start
    st.set_page_config(page_title="有梗.ai", page_icon="😏")
    st.title("😏 有梗.ai Team")

    st.sidebar.success("可选择角色单独命令其工作")

    # # history
    # msgs = ChatMessageHistory()
    # memory = ConversationBufferMemory(
    #     chat_memory=msgs, return_messages=True, memory_key="chat_history", output_key="output"
    # )
    # if len(msgs.messages) == 0: # or st.sidebar.button("Reset chat history"):
    #     msgs.clear()
    #     msgs.add_ai_message("How can I help you?")
    #     st.session_state.steps = {}

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # agent running
    if prompt := st.chat_input(placeholder="有梗，启动！"):
        st.chat_message("user").write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("assistant"):
            role = SimpleCoder()
            logger.info(prompt)
            result = asyncio.run(role.run(prompt))
            st.write(result)
            logger.info(result.content[:100])
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": result})

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
