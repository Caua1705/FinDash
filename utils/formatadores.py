import streamlit as st
import pandas as pd

def validar_colunas_necessarias(df):
    colunas_necessarias=["Data","Centro de Custo / Receita","Cliente / Fornecedor","Valor"]
    if not all(coluna in df.columns for coluna in colunas_necessarias):
            st.error("❌ A planilha deve conter as colunas: **Data**, **Centro de Custo / Receita**, **Valor** e **Cliente / Fornecedor**.")
            st.stop()

def formatar_colunas_dataframe(df) -> pd.DataFrame:
    df_formatado=df.copy()
    #Formatar coluna Data:
    try:
        df_formatado["Data"]=pd.to_datetime(df_formatado["Data"],dayfirst=True)
    except ValueError:
           st.error("❌ Erro na coluna **Data**. Revise os dados da tabela")
           st.stop()

    #Formatar coluna Centro de Custo / Receita:
    df_formatado["Centro de Custo / Receita"]=df_formatado["Centro de Custo / Receita"].fillna("Desconhecido")
    if df_formatado["Centro de Custo / Receita"].apply(lambda x: not isinstance(x,str)).any():
        st.error("❌ Erro na coluna **Centro de Custo / Receita**. Revise os dados da tabela")
        st.stop()

    #Formatar coluna Valor:
    try:
        df_formatado["Tipo"]=df_formatado["Valor"].apply(lambda x: "Receitas" if x > 0 else "Despesas")
        if (df_formatado["Valor"] > 0).all():
            st.error("❌ Erro na coluna **Valor**. Todos os valores são positivos")
            st.stop()
        if (df_formatado["Valor"] < 0).all():
            st.error("❌ Erro na coluna **Valor**. Todos os valores são negativos")
            st.stop()
        df_formatado["Valor"]=df_formatado["Valor"].apply(abs)
    except TypeError:
        st.error("❌ Erro na coluna **Valor**. Revise os dados da tabela")
        st.stop()

    #Formatar coluna Cliente / Fornecedor:
    df_formatado["Cliente / Fornecedor"]=df_formatado["Cliente / Fornecedor"].fillna("Desconhecido")
    if df_formatado["Cliente / Fornecedor"].apply(lambda x: not isinstance(x,str)).any():
        st.error("❌ Erro na coluna **Cliente / Fornecedor**. Revise os dados da tabela")
        st.stop()

    colunas_utilizadas=["Data","Centro de Custo / Receita","Cliente / Fornecedor","Tipo","Valor"]
    return df_formatado[colunas_utilizadas]