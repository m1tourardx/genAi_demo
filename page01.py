import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from scipy.stats import norm
import os
from PIL import Image

dir_database = os.path.join(os.getcwd(), 'database')
dir_imgs = os.path.join(os.getcwd(), 'imgs')


def third_page(doc01, doc02, doc03):
    col1, col2 = st.columns([0.2, 0.8])

    with col1:
        # TEG
        equipament_TEG = ['Contactor Tower', 'Reboiler', 'HX01']
        # Contactor Tower
        vars_contactor = ["Dew Point", "Contactor Pressure", "Natural Gas Moisture",
                          "Contactor Temperature", "Glycol Moisture", "Glycol Level"]
        # Reboiler
        vars_reboiler = ["Stripping Gas", "Pressure",
                         "Dry Glycol", "Glycol Flow", "Temperature"]
        # HX01
        vars_HX01 = ["Water Inlet Temperature", "Glycol Inlet Temperature",
                     "Out Glycol Temperature", "Out Water Temperature", "Heat Efficiency"]

        equipament = st.selectbox("Choose the equipament:", equipament_TEG)
        if equipament == "Contactor Tower":
            vars = st.selectbox("Choose the variables:", vars_contactor)
            data = doc01
            image = Image.open(os.path.join(dir_imgs, "contactor.jpeg"))
            st.image(image)

        elif equipament == "Reboiler":
            vars = st.selectbox("Choose the variables:", vars_reboiler)
            data = doc02
            image = Image.open(os.path.join(dir_imgs, "reboiler.jpeg"))
            st.image(image)
        elif equipament == "HX01":
            vars = st.selectbox("Choose the variables:", vars_HX01)
            data = doc03
            image = Image.open(os.path.join(dir_imgs, "hx.png"))
            st.image(image)

    with col2:
        df = data
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df.set_index('Timestamp', inplace=True)
        df.sort_index(inplace=True)

        view = st.selectbox("View Type:", ['TimeSeries', 'Data Distribution'])
        if view == 'TimeSeries':
            fig = px.line(
                df, y=vars, title=f"{vars} vs Timestamp", color_discrete_sequence=['red'])

        if view == 'Data Distribution':
            mean = df[vars].mean()
            std_dev = df[vars].std()
            x_range = np.linspace(df[vars].min(), df[vars].max(), 1000)
            normal_curve = norm.pdf(x_range, mean, std_dev)
            fig = px.histogram(
                df, x=vars, title=f"Distribution of {vars}", nbins=30, histnorm='probability density')
            fig.add_traces(go.Scatter(x=x_range, y=normal_curve, mode='lines',
                           name='Normal Distribution', line=dict(color='green')))

        st.plotly_chart(fig, use_container_width=True)
