import streamlit as st

def selecionar_data():
    data_inicial=st.sidebar.date_input("Data Inicial")
    data_final=st.sidebar.date_input("Data Final")
    if data_inicial>data_final:
        st.error("A data inicial não pode ser maior que a data final")
    return data_inicial,data_final

def filtrar_dados_data(df_formatado,data_inicial,data_final):
    df_filtrado=df_formatado.loc[(df_formatado["Data"].dt.date >= data_inicial ) &
                                    (df_formatado["Data"].dt.date <= data_final )]
    return df_filtrado

def selecionar_clientes_fornecedores(df_filtrado):
    df_clientes=df_filtrado[df_filtrado["Tipo"]=="Receitas"]
    df_fornecedores=df_filtrado[df_filtrado["Tipo"]=="Despesas"]
    return df_clientes,df_fornecedores