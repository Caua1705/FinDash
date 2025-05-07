import streamlit as st

def exibir_transacoes(df_filtrado):
  valores_pesquisa=df_filtrado.loc[df_filtrado["Cliente / Fornecedor"]!="Desconhecido",
                                                      "Cliente / Fornecedor"].unique()
  valor_escolhido=st.selectbox("Selecione um Cliente ou Fornecedor",valores_pesquisa)
  df_valor_escolhido=df_filtrado.loc[df_filtrado["Cliente / Fornecedor"]==valor_escolhido]
  st.write(df_valor_escolhido)
  st.success(f"💰 Total das Transações: R$ {df_valor_escolhido['Valor'].sum():,.2f}")