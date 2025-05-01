import plotly.express as px
import streamlit as st
import pandas as pd

def filtrar_dataframes_para_graficos(df_filtrado) -> tuple[pd.DataFrame,pd.DataFrame]:
    df_receitas_despesas=df_filtrado.pivot_table(index="Centro de Custo",
                                                       columns="Tipo",
                                                       values="Valor",
                                                       aggfunc="sum",
                                                       fill_value=0,
                                                       ).reset_index()
    df_receitas_despesas=df_receitas_despesas[["Centro de Custo","Receitas","Despesas"]]
    df_receitas_despesas=df_receitas_despesas.sort_values(by="Receitas",ascending=False)
    df_receitas_despesas.loc[len(df_receitas_despesas)] = ["TOTAL",df_receitas_despesas["Receitas"].sum(),df_receitas_despesas["Despesas"].sum()]
    receitas_mensais=df_filtrado.loc[df_filtrado["Tipo"]=="Receitas"]
    df_receitas_mensais=receitas_mensais.groupby("Centro de Custo")["Valor"].sum().sort_values(ascending=False).reset_index()
    df_receitas_mensais.loc[len(df_receitas_mensais)] = ["TOTAL",df_receitas_mensais["Valor"].sum()]
    return df_receitas_despesas,df_receitas_mensais

def gerar_graficos(df_receitas_despesas,df_receitas_mensais,filtro_mes) -> None:
    col1,col2=st.columns(2)
    with col1:    
        st.subheader("Total de Receitas e Despesas")
        fig1=px.bar(df_receitas_despesas,x="Centro de Custo",y=["Receitas","Despesas"],barmode="group",labels={"Categoria": "Categoria", "valor": "Valor"},title=f"Receitas e Despesas por Categoria em {filtro_mes}")
        fig1.update_layout(xaxis_tickangle=-45,xaxis_title="Categoria",yaxis_title="Valor",showlegend=True)
        col1.plotly_chart(fig1)
    with col2:               
        st.subheader("Categorias com maiores Receitas")
        if len(df_receitas_mensais)>2:
            df_receitas_mensais=df_receitas_mensais.loc[0:2]
        fig2=px.pie(df_receitas_mensais,names="Centro de Custo",values="Valor",title=f"Distribuição das maiores Receitas em {filtro_mes}",color="Centro de Custo")
        fig2.update_traces(textinfo="percent+label")       
        col2.plotly_chart(fig2)
    st.divider()

