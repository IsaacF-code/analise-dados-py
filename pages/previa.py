import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO

# Upload das bases
base_csv = st.file_uploader("Escolha as 2 bases para análise", accept_multiple_files=True, type='csv')

# Nome dos arquivos CSV
base_vgsales = "vgsales.csv"
base_games = "games.csv"

# Inicializa as variáveis das bases
df_vgsales = None
df_games = None

st.header("Todos os dados de cada tabela")

# Carrega os arquivos
if base_csv:
    for file in base_csv:
        bytes_data = file.getvalue()
        string_data = StringIO(bytes_data.decode("UTF-8"))
        base = pd.read_csv(string_data)

        if file.name == base_vgsales:
            df_vgsales = base
            df_vgsales['Year'] = pd.to_datetime(df_vgsales['Year'], format='%Y', errors='coerce')
            st.subheader(f"{file.name}")
            st.write(df_vgsales)
        
        elif file.name == base_games:
            df_games = base
            st.subheader(f"{file.name}")
            st.write(df_games)
