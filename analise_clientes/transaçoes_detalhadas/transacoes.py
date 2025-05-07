import streamlit as st

def exibir_transacoes(df_filtrado):
  st.write(df_filtrado)
  valores_pesquisa=df_filtrado.loc[df_filtrado["Cliente / Fornecedor"]!="Desconhecido",
                                                      "Cliente / Fornecedor"].unique()
  valor_escolhido=st.selectbox("Selecione um Cliente ou Fornecedor",valores_pesquisa)

  df_valor_escolhido=df_filtrado.loc[df_filtrado["Cliente / Fornecedor"]==valor_escolhido]

  df_valor_escolhido=df_valor_escolhido.drop(columns=["Mês"])
  df_valor_escolhido["Data"]=df_valor_escolhido["Data"].dt.date

  st.write(df_valor_escolhido)
  st.success(f"💰 Total das Transações: R$ {df_valor_escolhido['Valor'].sum():,.2f}")