import plotly.express as px
import streamlit as st
import pandas as pd

def filtrar_por_ano_mes(df_formatado) -> tuple[pd.DataFrame,str,str]:
    col1,col2=st.columns(2)
    numero_para_meses={1:"Janeiro",2:"Fevereiro",3:"Março",4:"Abril",5:"Maio",6:"Junho",7:"Julho",8:"Agosto",9:"Setembro",10:"Outubro",11:"Novembro",12:"Dezembro"}
    meses_para_numero={v:k for k, v in numero_para_meses.items()}
    ano=df_formatado["Data"].dt.year.unique()

    with col1:  
        filtro_ano=st.sidebar.selectbox("Selecione o ano:",ano)
        meses_disponiveis=df_formatado.loc[df_formatado["Data"].dt.year == filtro_ano,"Data"].dt.month.unique()
    with col2:  
        filtro_mes=st.sidebar.selectbox("Selecione o mês:",[numero_para_meses[mes] for mes in meses_disponiveis])
        df_filtrado=df_formatado.loc[(df_formatado["Data"].dt.year == filtro_ano) &
                                     (df_formatado["Data"].dt.month == meses_para_numero[filtro_mes])]
        data_filtrada=df_filtrado["Data"].iloc[0]
        data_referencia=data_filtrada.strftime("%Y-%m")

    mes_atual=meses_para_numero[filtro_mes]
    if mes_atual==1:
        ano_anterior=filtro_ano-1
        mes_anterior=12
    else:
        ano_anterior=filtro_ano
        mes_anterior=mes_atual-1
    df_filtrado_anterior=df_formatado.loc[(df_formatado["Data"].dt.year == ano_anterior) &
                                     (df_formatado["Data"].dt.month == mes_anterior)]
    return df_filtrado,df_filtrado_anterior,filtro_mes,data_referencia 

def agrupar_df_filtrado(df_filtrado,filtro_mes) -> pd.DataFrame:
    if (df_filtrado["Tipo"] =="Receitas").all(): 
        st.error(f"O mês de {filtro_mes} não possui despesas.")
        st.stop()
    if (df_filtrado["Tipo"]=="Despesas").all(): 
        st.error(f"O mês de {filtro_mes} não possui receitas.")
        st.stop()
    df_receitas_despesas=df_filtrado.pivot_table(index=["Centro de Custo / Receita","Data"],
                                                    columns="Tipo",
                                                    values="Valor",
                                                    aggfunc="sum",
                                                    fill_value=0,
                                                    ).reset_index()
    df_receitas_despesas=df_receitas_despesas[["Data","Centro de Custo / Receita","Receitas","Despesas"]]
    df_receitas_despesas=df_receitas_despesas.sort_values(by="Receitas",ascending=False)
    return df_receitas_despesas

def criacao_metricas(df_receitas_despesas,df_receitas_despesas_anterior):
    col1,col2,col3,col4=st.columns(4)
    with col1:
        total_receitas=df_receitas_despesas["Receitas"].sum()
        total_receitas_anterior=df_receitas_despesas_anterior["Receitas"].sum()
        delta_receitas=(total_receitas-total_receitas_anterior) / total_receitas_anterior * 100
        st.metric("Receita Total",f"R$ {total_receitas:,.2f}",f"{delta_receitas:.2f}%",delta_color="normal")
    with col2:
        total_despesas=df_receitas_despesas["Despesas"].sum()
        total_despesas_anterior=df_receitas_despesas_anterior["Despesas"].sum()
        delta_despesas=(total_despesas_anterior-total_despesas) / total_despesas_anterior * 100
        st.metric("Despesa Total",f"R$ {total_despesas:,.2f}",f"{delta_despesas:.2f}%",delta_color="inverse")
    with col3:
        saldo_liquido=total_receitas-total_despesas
        saldo_liquido_anterior=total_receitas_anterior-total_despesas_anterior
        delta_saldo=(saldo_liquido-saldo_liquido_anterior) / saldo_liquido_anterior * 100
        st.metric("Saldo Líquido",f"R$ {saldo_liquido:,.2f}",f"{delta_saldo:.2f}%",delta_color="normal")
    with col4:
        roi_consolidado=(saldo_liquido/total_despesas) * 100
        roi_consolidado_anterior=(saldo_liquido_anterior/total_despesas_anterior) * 100
        delta_roi= (roi_consolidado - roi_consolidado_anterior) / roi_consolidado_anterior * 100
        st.metric("ROI Consolidado",f"{roi_consolidado:,.2f}%",f"{delta_roi:.2f}%")
    st.divider()

def gerar_graficos(df_receitas_despesas,filtro_mes,df_formatado) -> None:
    # col1,col2=st.columns(2)
    # with col1:               
    st.subheader("Evolução Temporal das Receitas e Despesas")
    df_formatado["Mês"]=df_formatado["Data"].dt.month
    df_evolucao_temporal=df_formatado.groupby(["Mês","Tipo"])["Valor"].sum().reset_index()
    fig2=px.line(df_evolucao_temporal,x="Mês",y="Valor",color="Tipo")
    st.plotly_chart(fig2)
   
    # with col2:        
    fig1=px.bar(df_receitas_despesas,x="Centro de Custo / Receita",y=["Receitas","Despesas"],barmode="group",labels={"Categoria": "Categoria", "valor": "Valor"},title=f"Receitas e Despesas por Centro de Custo / Receita em {filtro_mes}")
    fig1.update_layout(xaxis_tickangle=-45,xaxis_title="Centro de Custo / Receita",yaxis_title="Valor",showlegend=True)
    st.plotly_chart(fig1)