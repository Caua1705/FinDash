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
    if "Receitas" in df_gerado.columns:
        df_gerado=df_gerado.sort_values(by="Receitas",ascending=False)
    else:
        df_gerado=df_gerado.sort_values(by="Despesas",ascending=False)
    return df_gerado

def criar_metricas(df_filtrado_clientes,df_filtrado_fornecedores,df_clientes):
    col1,col2,col3,col4=st.columns(4)
    #Top 1º Cliente:
    with col1:
      st.metric("Top 1 Cliente",df_filtrado_clientes.iloc[0,0], f"R$ {df_filtrado_clientes.iloc[0,1]:.2f}")
    with col2:
      st.metric("Principal Fornecedor",df_filtrado_fornecedores.iloc[0,0], f"R$ {df_filtrado_fornecedores.iloc[0,1]:.2f}")
    with col3:
      df_clientes=df_clientes.loc[df_clientes["Cliente / Fornecedor"]!="Desconhecido","Cliente / Fornecedor"]
      clientes_com_mais_transacoes=df_clientes.value_counts().reset_index()
      st.metric("Cliente com mais transações",clientes_com_mais_transacoes.iloc[0,0],f"{clientes_com_mais_transacoes.iloc[0,1]} transações")
    with col4:
      ticket_medio_cliente=df_filtrado_clientes["Receitas"].sum() / len(df_filtrado_clientes)
      st.metric("Ticket Médio por Cliente",f"R$ {ticket_medio_cliente:.2f}")
    st.divider()

def gerar_graficos(df_filtrado_clientes,df_filtrado_fornecedores):
        if len(df_filtrado_clientes)>10:
            df_filtrado_clientes=df_filtrado_clientes.iloc[:10]
        st.markdown("### Principais Clientes:")
        fig1=px.bar(df_filtrado_clientes,x="Receitas",y="Cliente / Fornecedor",title="Participação dos principais clientes nas receitas",color="Cliente / Fornecedor",orientation="h")
        fig1.update_layout(xaxis_title="Receitas",yaxis_title="Clientes",showlegend=False,height=370,bargap=0.3)
        st.plotly_chart(fig1,use_container_width=True)

        if len(df_filtrado_fornecedores)>10:
            df_filtrado_fornecedores=df_filtrado_fornecedores.iloc[:10]
        st.markdown("### Principais Fornecedores:")
        fig2=px.bar(df_filtrado_fornecedores,x="Despesas",y="Cliente / Fornecedor",title="Participação dos principais fornecedores nas despesas",color="Cliente / Fornecedor",orientation="h")
        fig2.update_layout(xaxis_title="Despesas",yaxis_title="Fornecedores",showlegend=False,height=370,bargap=0.3)
        st.plotly_chart(fig2,use_container_width=True)

def transacoes_detalhadas(df_filtrado):
    valor_pesquisa=st.text_input("Pesquisar Cliente/Fornecedor",df_filtrado["Cliente / Fornecedor"].str())
    st.write(valor_pesquisa)
    