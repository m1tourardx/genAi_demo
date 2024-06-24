import streamlit as st
from page02 import second_page
from page01 import third_page
from chatbot import chat
from PIL import Image
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from tools import ContactorQuery, HeatQuery
from openai import OpenAI
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import pandas as pd

dir_database = os.path.join(os.getcwd(), 'database')
def update_timestamps_in_datasets(directory):
    files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    reference_date = datetime.today().date()
    
    updated_datasets = {}

    for file in files:
        df = pd.read_csv(os.path.join(directory, file))
        
        last_timestamp = pd.to_datetime(df['Timestamp'].iloc[-1]).date()
        days_diff = (reference_date - last_timestamp).days

        df['Timestamp'] = pd.to_datetime(df['Timestamp']) + timedelta(days=days_diff)
        
        updated_datasets[file] = df
        
    return updated_datasets

updated_datasets = update_timestamps_in_datasets(dir_database)
doc01 = updated_datasets.get('contactor_tower.csv')
doc02 = updated_datasets.get('reboiler.csv')
doc03 = updated_datasets.get('heat_exchanger.csv')

dir_imgs = os.path.join(os.getcwd(), 'imgs')

st.set_page_config(page_title="RadixAi", page_icon=":tada:", layout="wide")

st.markdown("""
    <style>
    /* Ajusta o padding do topo do conteúdo principal */
    .main .block-container {
        padding-top: 3rem; /* Ajuste para um valor pequeno para reduzir o espaço, não use valores negativos */
    }
    /* Opcional: ajusta o padding do cabeçalho para reduzir o espaço, se necessário */
    header {
        padding-top: -2rem;
        padding-bottom: 0rem;
    }
    /* Tenta reduzir o espaço acima das abas */
    .stTabs {
        margin-top: -20px; /* Ajuste negativo para tentar puxar as abas para mais perto do conteúdo acima */
    }
    </style>
""", unsafe_allow_html=True)

image = Image.open(os.path.join(dir_imgs, "RDX_top.png"))
st.image(image, use_column_width=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Main", "Documents Database", "Application Catalog", "Architecture", "Natural Gas Dehydration Process"])
with tab1:
    third_page(doc01, doc02, doc03)

with tab2:
    second_page()

with tab3:
    col1, col2, col3 = st.columns([0.15, 0.7, 0.15])
    with col1:
        ''
    with col2:
        image = Image.open(os.path.join(dir_imgs, "aplications.png"))
        st.image(image, use_column_width=True)
    with col3:
        ''

with tab4:
    col1, col2, col3 = st.columns([0.15, 0.7, 0.15])
    with col1:
        ''
    with col2:
        image = Image.open(os.path.join(dir_imgs, "model.png"))
        st.image(image, use_column_width=True)
    with col3:
        ''

with tab5:
    col1, col2, col3 = st.columns([0.15, 0.7, 0.15])
    with col1:
        ''
    with col2:
        image = Image.open(os.path.join(dir_imgs, "TEG.png"))
        st.image(image, use_column_width=True)
    with col3:
        ''

chat()
