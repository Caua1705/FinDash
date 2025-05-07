import pandas as pd
import streamlit as st

def agrupar_dados(df):
    df_agrupado=pd.pivot_table(df,
                             values="Valor",
                             columns="Tipo",
                             index="Cliente / Fornecedor",
                             aggfunc="sum").reset_index()
    
    df_agrupado=df_agrupado.loc[df_agrupado["Cliente / Fornecedor"]!="Desconhecido"]
    if "Receitas" in df_agrupado.columns:
        df_agrupado=df_agrupado.sort_values(by="Receitas",ascending=False)
    else:
        df_agrupado=df_agrupado.sort_values(by="Despesas",ascending=False)
    return df_agrupado
