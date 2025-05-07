import streamlit as st
import pandas as pd

def obter_filtros_ano_mes(df_formatado) -> tuple[pd.DataFrame,str,str]:
    numero_para_meses={1:"Janeiro",2:"Fevereiro",3:"Março",4:"Abril",
                       5:"Maio",6:"Junho",7:"Julho",8:"Agosto",9:"Setembro",
                       10:"Outubro",11:"Novembro",12:"Dezembro"}
    
    meses_para_numero={v:k for k, v in numero_para_meses.items()}

    anos=df_formatado["Data"].dt.year.unique()
    with st.sidebar:
        st.markdown("### Filtros")
        filtro_ano=st.selectbox("Ano",anos)
        meses_disponiveis=df_formatado.loc[df_formatado["Data"].dt.year == filtro_ano,"Data"].dt.month.unique()
        filtro_mes=st.selectbox("Mês:",[numero_para_meses[mes] for mes in meses_disponiveis])

    mes_selecionado_numero=meses_para_numero[filtro_mes]
    data_formatada=f"{filtro_ano}-{mes_selecionado_numero:02d}"

    return {"ano_escolhido": filtro_ano,
        "mes_escolhido_nome": filtro_mes,
        "mes_escolhido_numero": mes_selecionado_numero,
        "data_formatada": data_formatada,
        "numero_para_meses": numero_para_meses}

def filtrar_dados_ano_mes(df_formatado,filtro_ano,mes_selecionado_numero):

    df_filtrado=df_formatado.loc[(df_formatado["Data"].dt.year == filtro_ano) &
                                (df_formatado["Data"].dt.month == mes_selecionado_numero)]
    
    if mes_selecionado_numero==1:
        ano_anterior=filtro_ano-1
        mes_anterior=12
    else:
        ano_anterior=filtro_ano
        mes_anterior=mes_selecionado_numero-1

    df_filtrado_anterior=df_formatado.loc[(df_formatado["Data"].dt.year == ano_anterior) &
                                    (df_formatado["Data"].dt.month == mes_anterior)]
    return df_filtrado,df_filtrado_anterior