import streamlit as st
import pandas as pd
from utils.formatadores import validar_colunas_necessarias, formatar_colunas_dataframe

# Configurações da página
st.set_page_config(
    page_title="FinDash",
    layout="wide",
    page_icon="💸"
)

# Cabeçalho visual
st.markdown("## 💹 **FinDash - Painel Financeiro Inteligente**")

st.markdown("""
Bem-vindo ao **FinDash**, sua central de controle financeiro!

🔍 **Explore as opções no menu lateral** para:
- 📈 Visão Geral de Receitas e Despesas  
- 🧾 Análise por Cliente e Fornecedor  

Faça upload da sua planilha financeira para começar.
""")

# Upload do arquivo
st.markdown("### 📁 **Importar Planilha Financeira**")
upload_planilha = st.file_uploader(
    "Selecione um arquivo no formato `.csv` ou `.xlsx`:",
    type=["xlsx", "csv"]
)

# Processamento do arquivo
if upload_planilha is not None:
    if upload_planilha.name.endswith("xlsx"):
        df = pd.read_excel(upload_planilha)
    elif upload_planilha.name.endswith("csv"):
        df = pd.read_csv(upload_planilha)

    validar_colunas_necessarias(df)
    df_formatado = formatar_colunas_dataframe(df)

    st.success("✅ Arquivo carregado e processado com sucesso!")

    with st.expander("👁️ Pré-visualizar dados carregados"):
        st.dataframe(df_formatado, use_container_width=True)

    st.session_state.df_formatado = df_formatado
else:
    st.info("⬅️ Faça o upload de um arquivo para continuar.")