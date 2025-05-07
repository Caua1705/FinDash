import streamlit as st

def criar_metricas(df_clientes,df_fornecedores):
    col1,col2,col3,col4=st.columns(4)

    with col1:
      principal_cliente=df_clientes.iloc[0,0]
      valor_principal_cliente=df_clientes.iloc[0,1]
      st.metric("Top 1 Cliente",principal_cliente, f"R$ {valor_principal_cliente:.2f}")

    with col2:
      principal_fornecedor=df_fornecedores.iloc[0,0]
      valor_principal_fornecedor=df_fornecedores.iloc[0,1]
      st.metric("Principal Fornecedor",principal_fornecedor, f"R$ {valor_principal_fornecedor:.2f}")

    with col3:
      ticket_medio_cliente=df_clientes["Receitas"].sum() / len(df_clientes)
      st.metric("Ticket Médio por Cliente",f"R$ {ticket_medio_cliente:.2f}")

    with col4:
      qntd_clientes_ativos=len(df_clientes)
      st.metric("Clientes Ativos",qntd_clientes_ativos)
