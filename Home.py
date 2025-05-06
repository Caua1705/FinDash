import streamlit as st
import pandas as pd
from utils.formatadores import validar_colunas_necessarias,formatar_colunas_dataframe

st.set_page_config(page_title="FinDash",layout="wide",page_icon="💼") 

st.title("💼 FinDash ")
st.markdown("##### Seu painel financeiro inteligente")

st.markdown("""
➡️ Use o menu lateral esquerdo para acessar as funcionalidades:
- 📊 Visão Geral de Receitas e Despesas
- 📈 Análise por Cliente e Fornecedor
""")

st.markdown("##### 📁 Carregue sua planilha financeira (.CSV ou .XLSX)")
upload_planilha=st.file_uploader("Selecione o arquivo:",accept_multiple_files=False,type=["xlsx","csv"])

if upload_planilha is not None:
    if upload_planilha.name.endswith("xlsx"):
        df=pd.read_excel(upload_planilha)
    if upload_planilha.name.endswith("csv"):
        df=pd.read_csv(upload_planilha)

    validar_colunas_necessarias(df)
    df_formatado=formatar_colunas_dataframe(df)

    st.success("✅Arquivo carregado com sucesso!")
    st.subheader("Pré-visualização dos dados formatados:")
    st.write(df_formatado.head(15))
    st.session_state.df_formatado=df_formatado

