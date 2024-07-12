import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pandas_agent import CustomAgent
import os
from dotenv import load_dotenv

load_dotenv()

def chat(agent_executor):
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm here to help you find information about biomass gasification processes with supercritical water."}]

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
                    response = agent_executor.agent_exec(prompt)
                    st.write(response)
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message)

def plot_surface(x, y, z, title):
    x_array = np.array(x)
    y_array = np.array(y)
    z_array = np.array(z)

    x_grid, y_grid = np.meshgrid(np.unique(x_array), np.unique(y_array))
    z_grid = z_array.reshape(len(np.unique(y_array)), len(np.unique(x_array)))

    fig = go.Figure(data=[go.Surface(z=z_grid, x=np.unique(x_array), y=np.unique(y_array), colorscale='Viridis')])

    fig.update_layout(
        scene=dict(
            xaxis_title='Temperature (K)',
            yaxis_title='Pressure (bar)',
            zaxis_title=title
        ),
        autosize=True,
        margin=dict(l=65, r=50, b=65, t=90)
    )

    st.plotly_chart(fig, use_container_width=True)

st.title("LLM Tuned as Agent")
st.write("---")

data = pd.read_csv('data.csv')

z_var = st.selectbox("Choose the variable:", data.columns)
plot_surface(data['Temperature (K)'], data['Pressure (bar)'], data[z_var], z_var)

# Model selection
model_selection = st.selectbox("Choose a model:", ["SCWG model", "GPT-3.5-turbo"])

if model_selection == "SCWG model":
    azure_deployment = os.getenv("DEPLOY_MODEL_01")
else:
    azure_deployment = os.getenv("DEPLOY_MODEL_02")

agent_executor = CustomAgent(azure_deployment)
st.write("---")

chat(agent_executor)