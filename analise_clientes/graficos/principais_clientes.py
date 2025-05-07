import streamlit as st
import plotly.express as px

def exibir_grafico_principais_clientes(df_agrupado_clientes):
  st.markdown("### 📊 Principais Clientes")
  if len(df_agrupado_clientes)>10:
      df_agrupado_clientes=df_agrupado_clientes.iloc[:10]
  fig1=px.bar(df_agrupado_clientes,x="Receitas",y="Cliente / Fornecedor",
              title="Top 10 Clientes por Receita",
              color="Cliente / Fornecedor",orientation="h")
  fig1.update_layout(xaxis_title="Receitas",yaxis_title="Clientes",showlegend=False,height=370,bargap=0.3)
  st.plotly_chart(fig1,use_container_width=True)


