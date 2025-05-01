import pandas as pd
import streamlit as st

def carregar_arquivo():
    st.set_page_config(page_title="FinDash",layout="wide",page_icon="💲") 
    st.title("Dashboard Financeiro:")
    st.write("Escolha um arquivo do tipo CSV ou XLSX para carregar a planilha:")
    upload_planilha=st.file_uploader("Selecione o arquivo:",accept_multiple_files=False,type=["xlsx","csv"])
    return upload_planilha

def carregar_dataframe(arquivo) -> pd.DataFrame:
    if arquivo.name.endswith("xlsx"):
        df=pd.read_excel(arquivo)
    if arquivo.name.endswith("csv"):
        df=pd.read_csv(arquivo)
    return df

def selecionar_colunas_dataframe(df) -> dict[str,pd.DataFrame]:
    col1,col2,col3=st.columns(3)
    with col1:
        coluna_data=st.selectbox("Selecione a coluna Data(dd/mm/yyyy)",list(df.columns),help="Coluna onde está a data da transação")
    with col2:
        coluna_centro_custo=st.selectbox("Selecione a coluna Centro de Custo",[a for a in list(df.columns) if a != coluna_data],help="Coluna onde está o centro de custo da transação")
    with col3:
        coluna_valor=st.selectbox("Selecione a coluna Valor",[a for a in list(df.columns) if a != coluna_data and a != coluna_centro_custo],help="Coluna onde está o valor da transação")
    dict_colunas={"Data":coluna_data,"Centro de Custo":coluna_centro_custo,"Valor":coluna_valor}
    return dict_colunas
        
def formatar_colunas_dataframe(df,colunas_dataframe) -> pd.DataFrame:
    df_formatado=df.copy()
    df_formatado=df_formatado.rename(columns={colunas_dataframe["Data"] :"Data",
                                      colunas_dataframe["Centro de Custo"] :"Centro de Custo",
                                      colunas_dataframe["Valor"] : "Valor"
                                      })
    df_formatado=df_formatado[["Data","Centro de Custo","Valor"]]   
    df_formatado["Centro de Custo"]=df_formatado["Centro de Custo"].fillna("Desconhecido")
    try:
        coluna_formatada=pd.to_datetime(df_formatado["Data"],dayfirst=True) 
    except ValueError:
           st.error(f"Erro na coluna Data. Revise os dados da tabela")
           st.stop()
    if df_formatado["Centro de Custo"].apply(lambda x: not isinstance(x,str)).any():
        st.error(f"Erro na coluna Centro de Custo. Revise os dados da tabela")
        st.stop()
    try:
        df_formatado["Tipo"]=df_formatado["Valor"].apply(lambda x: "receita" if x > 0 else "despesa")
        if df_formatado["Valor"].apply(lambda x: x > 0 ).all():
            st.error(f"Erro na coluna valor. Todos os valores são positivos")
            st.stop()
        if df_formatado["Valor"].apply(lambda x: x < 0 ).all():
            st.error(f"Erro na coluna valor. Todos os valores são negativos")
            st.stop()
    except TypeError:
        st.error(f"Erro na coluna Valor(R$). Revise os dados da tabela")
        st.stop()
    df_formatado["Data"]=coluna_formatada
    df_formatado["Valor"]=df_formatado["Valor"].apply(abs)
    return df_formatado

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

