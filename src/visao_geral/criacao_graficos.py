import plotly.express as px
import streamlit as st
import pandas as pd

def filtrar_df_formatado_por_ano_mes(df_formatado) -> tuple[pd.DataFrame,str,str]:
    col1,col2=st.columns(2)
    numero_para_meses={1:"Janeiro",2:"Fevereiro",3:"Março",4:"Abril",5:"Maio",6:"Junho",7:"Julho",8:"Agosto",9:"Setembro",10:"Outubro",11:"Novembro",12:"Dezembro"}
    meses_para_numero={v:k for k, v in numero_para_meses.items() }
    ano=df_formatado["Data"].dt.year.unique()
    with col1:  
        filtro_ano=st.selectbox("Selecione o ano:",ano)
        meses_disponiveis=df_formatado.loc[df_formatado["Data"].dt.year == filtro_ano,"Data"].dt.month.unique()
    with col2:  
        filtro_mes=st.selectbox("Selecione o mês:",[numero_para_meses[mes] for mes in meses_disponiveis])
        df_filtrado=df_formatado.loc[(df_formatado["Data"].dt.year == filtro_ano) &
                                     (df_formatado["Data"].dt.month == meses_para_numero[filtro_mes])]
        data_filtrada=df_filtrado["Data"].iloc[0]
        data_referencia=data_filtrada.strftime("%Y-%m")
    return df_filtrado,filtro_mes,data_referencia 

def filtrar_dataframes_para_graficos(df_filtrado,filtro_mes) -> tuple[pd.DataFrame,pd.DataFrame]:
    if (df_filtrado["Tipo"] =="Receitas").all(): 
        st.error(f"O mês de {filtro_mes} não possui despesas.")
        st.stop()
    if (df_filtrado["Tipo"]=="Despesas").all(): 
        st.error(f"O mês de {filtro_mes} não possui receitas.")
        st.stop()
    df_receitas_despesas=df_filtrado.pivot_table(index="Centro de Custo / Receita",
                                                    columns="Tipo",
                                                    values="Valor",
                                                    aggfunc="sum",
                                                    fill_value=0,
                                                    ).reset_index()
    df_receitas_despesas=df_receitas_despesas[["Centro de Custo / Receita","Receitas","Despesas"]]
    df_receitas_despesas=df_receitas_despesas.sort_values(by="Receitas",ascending=False)
    df_receitas_despesas.loc[len(df_receitas_despesas)] = ["TOTAL",df_receitas_despesas["Receitas"].sum(),df_receitas_despesas["Despesas"].sum()]
    receitas_mensais=df_filtrado.loc[df_filtrado["Tipo"]=="Receitas"]
    df_receitas_mensais=receitas_mensais.groupby("Centro de Custo / Receita")["Valor"].sum().sort_values(ascending=False).reset_index()
    df_receitas_mensais.loc[len(df_receitas_mensais)] = ["TOTAL",df_receitas_mensais["Valor"].sum()]
    return df_receitas_despesas,df_receitas_mensais

def gerar_graficos(df_receitas_despesas,df_receitas_mensais,filtro_mes) -> None:
    col1,col2=st.columns(2)
    with col1:    
        st.subheader("Total de Receitas e Despesas")
        fig1=px.bar(df_receitas_despesas,x="Centro de Custo / Receita",y=["Receitas","Despesas"],barmode="group",labels={"Categoria": "Categoria", "valor": "Valor"},title=f"Receitas e Despesas por Centro de Custo / Receita em {filtro_mes}")
        fig1.update_layout(xaxis_tickangle=-45,xaxis_title="Categoria",yaxis_title="Valor",showlegend=True)
        col1.plotly_chart(fig1)
    with col2:               
        st.subheader("Centros de Receita com maiores receitas")
        if len(df_receitas_mensais)>2:
            df_receitas_mensais=df_receitas_mensais.loc[0:2]
        fig2=px.pie(df_receitas_mensais,names="Centro de Custo / Receita",values="Valor",title=f"Distribuição das maiores Receitas em {filtro_mes}",color="Centro de Custo / Receita")
        fig2.update_traces(textinfo="percent+label")       
        col2.plotly_chart(fig2)
    st.divider()

