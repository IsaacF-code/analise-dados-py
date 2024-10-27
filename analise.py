import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO

# Upload das bases
base_csv = st.file_uploader("Escolha as 2 bases para análise", accept_multiple_files=True, type='csv')

# Nome dos arquivos CSV
base_vgsales = "vgsales.csv"
base_games = "games.csv"

if base_csv != None:
    for file in base_csv:
        bytes_data = file.getvalue()
        string_data = StringIO(bytes_data.decode("UTF-8"))
        base = pd.read_csv(string_data)

        st.header(f"Prévia dos dados - {file.name}")
        base

    # Pegando coluna data da base vgsales
    if file.name == base_vgsales:
        base['Year'] = pd.to_datetime(base['Year'], format='%Y', errors='coerce')
        
        if base['Year'].isnull().any():
            st.write("Alguns não poderam ser convertidos")

        # Extrair anos
        anos = base['Year'].dt.to_period('Y').unique()

        st.sidebar.header("Filtros")

        # Filtro anos
        ano_selecionado = st.sidebar.selectbox(
            "Ano",
            anos.astype(str),
            index=None,
            placeholder="Selecione o ano"
        )

        base_filtrada_vg = base[base['Year'].dt.to_period('Y').astype(str) == ano_selecionado]
        
        # Agrupando ano e nome da base vgsales
        data_nome = base_filtrada_vg.groupby(['Year', 'Name']).reset()


        st.write(data_nome)