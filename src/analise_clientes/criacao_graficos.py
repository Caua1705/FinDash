import streamlit as st
import pandas as pd
import plotly.express as px

def filtrar_dataframes_para_graficos(df_filtrado_para_grafico):
    df_gerado=pd.pivot_table(df_filtrado_para_grafico,
                                        values="Valor",
                                        columns="Tipo",
                                        index="Cliente / Fornecedor",
                                        aggfunc="sum").reset_index()
    df_gerado=df_gerado.loc[df_gerado["Cliente / Fornecedor"]!="Desconhecido"]
    return df_gerado

def gerar_graficos(df_filtrado_clientes,df_filtrado_fornecedores):
    col1,col2=st.tabs(["Visão Geral", "Detalhes por Cliente/Fornecedor"])
    with col1:
        df_filtrado_clientes=df_filtrado_clientes.sort_values(by="Receitas",ascending=False)
        if len(df_filtrado_clientes)>10:
            df_filtrado_clientes=df_filtrado_clientes.iloc[:10]
        st.subheader("Distribuição de Receitas por Cliente")
        fig1=px.bar(df_filtrado_clientes,x="Receitas",y="Cliente / Fornecedor",title="Participação dos principais clientes nas receitas",color="Cliente / Fornecedor",orientation="h")
        fig1.update_layout(xaxis_title="Receitas",yaxis_title="Clientes",showlegend=False,height=370,bargap=0.3)
        col1.plotly_chart(fig1)
    with col2:
        df_filtrado_fornecedores=df_filtrado_fornecedores.sort_values(by="Despesas",ascending=False)
        if len(df_filtrado_fornecedores)>5:
            df_filtrado_fornecedores=df_filtrado_fornecedores.iloc[:10]
        st.subheader("Distribuição de Despesas por Fornecedor")
        fig1=px.bar(df_filtrado_fornecedores,x="Despesas",y="Cliente / Fornecedor",title="Participação dos principais fornecedores nas despesas",color="Cliente / Fornecedor",orientation="h")
        fig1.update_layout(xaxis_title="Despesas",yaxis_title="Fornecedores",showlegend=False,height=370,bargap=0.3)
        col2.plotly_chart(fig1)
        