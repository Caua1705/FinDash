import streamlit as st
import plotly.express as px

def exibir_grafico_evolucao_mensal(df_evolucao_mensal):
    st.subheader("Evolução Mensal")
    fig2=px.line(df_evolucao_mensal,x="Mês",y="Valor",color="Tipo",markers=True)
    fig2.update_layout(title="Evolução Mensal de Receitas e Despesas",xaxis_title="Mês",yaxis_title="Valor",showlegend=True)
    st.plotly_chart(fig2,use_container_width=True)