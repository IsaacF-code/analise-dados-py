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

col1, col2 = st.columns(spec=2)

# Carrega os arquivos
if base_csv:
    for file in base_csv:
        bytes_data = file.getvalue()
        string_data = StringIO(bytes_data.decode("UTF-8"))
        base = pd.read_csv(string_data)

        if file.name == base_vgsales:
            df_vgsales = base
            df_vgsales['Year'] = pd.to_datetime(df_vgsales['Year'], format='%Y', errors='coerce')
            with col1:
                st.header(f"Prévia dos dados - {file.name}")
                st.write(df_vgsales.head())
        
        elif file.name == base_games:
            df_games = base
            with col2:
                st.header(f"Prévia dos dados - {file.name}")
                st.write(df_games.head())

    # Verifica se ambas as bases foram carregadas
    if df_vgsales is not None and df_games is not None:
        # Filtra dados que possuem valores de "Year" não nulos na base vgsales
        df_vgsales = df_vgsales.dropna(subset=['Year'])
        
        
        anos = df_vgsales['Year'].dt.to_period('Y').unique()
        anos = ["Todos os anos"] + list(anos.astype(str))

        st.sidebar.header("Filtros")
        ano_selecionado = st.sidebar.selectbox(
            "Ano",
            anos,
            index=0,
            placeholder="Selecione o ano"
        )

        if ano_selecionado == "Todos os anos":
            df_vgsales_filtrada = df_vgsales
        else:
            # Filtra os dados pelo ano selecionado na base vgsales
            df_vgsales_filtrada = df_vgsales[df_vgsales['Year'].dt.to_period('Y').astype(str) == ano_selecionado]

        # Faz a fusão das bases usando as colunas de nome (Name e Title)
        df_fusionada = pd.merge(
            df_vgsales_filtrada,
            df_games,
            how='inner',
            left_on='Name',
            right_on='Title'
        )

        # 
        st.write("Dados combinados para o ano selecionado:")
        st.write(df_fusionada[['Year', 'Name', 'Global_Sales', 'Title']])
        
        # Vendas globais
        fig_vendas_globais = px.bar(df_fusionada, x='Title', y='Global_Sales', title=f"Vendas Globais dos Jogos - {ano_selecionado} - (Em Milhões)")
        st.plotly_chart(fig_vendas_globais)

        # Rating com plotly
        fig_aval_media = px.bar(df_fusionada, x='Name', y='Rating', title="Classificação do jogos")
        st.plotly_chart(fig_aval_media)

        # Rating com stream
        st.bar_chart(df_fusionada, x="Name", y="Rating") 
