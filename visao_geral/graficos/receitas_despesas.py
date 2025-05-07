import streamlit as st
import plotly.express as px

def exibir_grafico_receitas_despesas(df_receitas_despesas,filtro_mes) -> None:   
    st.subheader("Total de Receitas e Despesas")
    fig1=px.bar(df_receitas_despesas,x="Centro de Custo / Receita",y=["Receitas","Despesas"],barmode="group",labels={"Categoria": "Categoria", "valor": "Valor"},title=f"Receitas e Despesas por Centro de Custo / Receita em {filtro_mes}")
    fig1.update_layout(xaxis_tickangle=-45,xaxis_title="Centro de Custo / Receita",yaxis_title="Valor",showlegend=True)
    st.plotly_chart(fig1,use_container_width=True)