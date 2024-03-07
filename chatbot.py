import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from agent_handler import CustomAgent


def chat():
    # Cria uma instância do agente executor
    agent_executor = CustomAgent().agent_exec()

    if "messages" not in st.session_state.keys():
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm the chatbot and I can help you with queries regarding information about processes and documents. How can I help you?"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking ... "):
                response = agent_executor.invoke({"input": prompt})['output']
                st.write(response)
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)
