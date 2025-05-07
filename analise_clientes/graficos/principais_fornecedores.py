import streamlit as st
import plotly.express as px

def exibir_grafico_principais_fornecedores(df_agrupado_fornecedores):
  st.markdown("### 📉 Principais Fornecedores")
  if len(df_agrupado_fornecedores)>10:
      df_agrupado_fornecedores=df_agrupado_fornecedores.iloc[:10]
  fig2=px.bar(df_agrupado_fornecedores,x="Despesas",y="Cliente / Fornecedor",title="Top 10 Fornecedores por Despesa",color="Cliente / Fornecedor",orientation="h")
  fig2.update_layout(xaxis_title="Despesas",yaxis_title="Fornecedores",showlegend=False,height=370,bargap=0.3)
  st.plotly_chart(fig2,use_container_width=True)
  st.divider()
