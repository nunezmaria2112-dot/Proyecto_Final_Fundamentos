import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard de Accidentes de Tránsito", layout="wide")

st.title("Dashboard de Accidentes de Tránsito")

@st.cache_data
def load_data():
    df = pd.read_csv("dataset_traffic_acciden_prediction_final.csv")

