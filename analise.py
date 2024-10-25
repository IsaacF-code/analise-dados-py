import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO

base_csv = st.file_uploader("Escolha as 2 bases para análise", accept_multiple_files=True, type='csv')

if base_csv != None:
    for file in base_csv:
        bytes_data = base_csv.getvalue()
        string_data = StringIO(bytes_data.decode("UTF-8"))
        base = pd.read_csv(string_data)

        st.header("Prévia dos dados - {file.name}")
        base
    
