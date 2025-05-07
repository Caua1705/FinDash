import streamlit as st
from datetime import datetime,timedelta

def selecionar_data():
    agora=datetime.now()
    data_inicial=st.sidebar.date_input("Data Inicial",agora - timedelta(days=30))
    data_final=st.sidebar.date_input("Data Final")
    if data_inicial>data_final:
        st.error("A Data Inicial não pode ser maior que a Data Final.",agora)
        st.stop()
    return data_inicial,data_final

def filtrar_dados_data(df_formatado,data_inicial,data_final):
    df_filtrado=df_formatado.loc[(df_formatado["Data"].dt.date >= data_inicial ) &
                                    (df_formatado["Data"].dt.date <= data_final )]
    if df_filtrado.empty:
        st.error(f"Nenhum dado encontrado para o período entre {data_inicial.strftime("%d/%m/%Y")} e {data_final.strftime("%d/%m/%Y")}")
        st.stop()
    return df_filtrado

def selecionar_clientes_fornecedores(df_filtrado):
    df_clientes=df_filtrado[df_filtrado["Tipo"]=="Receitas"]
    df_fornecedores=df_filtrado[df_filtrado["Tipo"]=="Despesas"]
    return df_clientes,df_fornecedores