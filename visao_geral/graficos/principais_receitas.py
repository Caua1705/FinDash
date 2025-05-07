import streamlit as st
import plotly.express as px

def exibir_grafico_principais_receitas(df_receitas_mensais,filtro_mes):
    st.subheader("Principais Receitas")
    if len(df_receitas_mensais)>2:
            df_receitas_mensais=df_receitas_mensais.loc[0:2]
    fig2=px.pie(df_receitas_mensais,names="Centro de Custo / Receita",values="Valor",title=f"Distribuição das maiores Receitas em {filtro_mes}",color="Centro de Custo / Receita")
    fig2.update_traces(textinfo="percent+label")       
    st.plotly_chart(fig2,use_container_width=True)
    