import pandas as pd
from pathlib import Path
import streamlit as st
import tempfile
import plotly.express as px

def configurar_upload():
    page_config=st.set_page_config(page_title="FinDash",layout="wide",page_icon="💲") 
    st.title("Planilha Financeira:")
    st.write("Escolha um arquivo do tipo CSV ou XLSX para carregar a planilha:")
    upload_planilha=st.file_uploader("Selecione o arquivo:",accept_multiple_files=False,type=["xlsx","csv"])
    return upload_planilha

def carregar_dataframe(arquivo) -> tuple[pd.DataFrame,str]:
    with tempfile.TemporaryDirectory() as dir_temp:
        dir_temp=Path(dir_temp) / arquivo.name
        with open(dir_temp, mode="wb") as escritor:
            escritor.write(arquivo.read())
        if arquivo.name.endswith("xlsx"):
            df=pd.read_excel(dir_temp)
            tipo="xlsx"
        if arquivo.name.endswith("csv"):
            df=pd.read_csv(dir_temp)
            tipo="csv"
    return df,tipo

def selecionar_colunas(df) -> tuple[dict[str,str], bool]:
    columns=st.sidebar
    columns.write("### Seleção de Colunas:")
    coluna_data=columns.selectbox("Selecione a coluna Data",list(df.columns),help="Coluna onde está a data da transação")
    coluna_categoria=columns.selectbox("Selecione a coluna Categoria",[a for a in list(df.columns) if a != coluna_data],help="Coluna onde está a Categoria da transação")
    coluna_tipo=columns.selectbox("Selecione a coluna Tipo(Receita/Despesa)",[a for a in list(df.columns) if a != coluna_data and a != coluna_categoria],help="Coluna onde está a tipo da transação")
    coluna_valor=columns.selectbox("Selecione a coluna Valor",[a for a in list(df.columns) if a != coluna_data and a != coluna_categoria and a != coluna_tipo],help="Coluna onde está o valor da transação")
    visualizar_dashboard=columns.button("Visualizar Dashboard")
    if "colunas_selecionadas" not in st.session_state:
        st.session_state.colunas_selecionadas=False
    if visualizar_dashboard:
        st.session_state.colunas_selecionadas=True
    dict_colunas={"Data":coluna_data,
                  "Categoria":coluna_categoria,
                  "Tipo":coluna_tipo,
                  "Valor":coluna_valor}
    return dict_colunas,st.session_state.colunas_selecionadas

def formatar_colunas(df,colunas_dataframe) -> pd.DataFrame:
    df_formatado=df.copy()
    df_formatado=df_formatado.rename(columns={colunas_dataframe["Data"] :"Data",
                                      colunas_dataframe["Categoria"] :"Categoria",
                                      colunas_dataframe["Tipo"] : "Tipo",
                                      colunas_dataframe["Valor"] : "Valor"
                                      })
    formatacao_letras_tipo=df_formatado["Tipo"].str.lower()
    formatacao_letras_categoria=df_formatado["Categoria"].str.lower()
    coluna_formatada=pd.to_datetime(df_formatado["Data"],dayfirst=True) #Formata a coluna data do DataFrame
    df_formatado["Tipo"]=formatacao_letras_tipo
    df_formatado["Categoria"]=formatacao_letras_categoria
    df_formatado["Data"]=coluna_formatada
    return df_formatado

def filtrar_df_formatado(df_formatado) -> pd.DataFrame:
    col1,col2=st.columns(2)
    ano=df_formatado["Data"].dt.year.unique()
    dict_meses={1:"Janeiro",2:"Fevereiro",3:"Março",4:"Abril",5:"Maio",6:"Junho",7:"Julho",8:"Agosto",9:"Setembro",10:"Outubro",11:"Novembro",12:"Dezembro"}
    with col1:  
        filtro_ano=st.selectbox("Selecione o ano:",ano)
        meses_disponiveis=df_formatado.loc[df_formatado["Data"].dt.year == filtro_ano,"Data"].dt.month.unique()
    with col2:  
        filtro_mes=st.selectbox("Selecione o mês:",[dict_meses[mes] for mes in meses_disponiveis])
        df_filtrado=df_formatado.loc[(df_formatado["Data"].dt.year == filtro_ano) &
                                 (df_formatado["Data"].dt.month == [k for k, v in dict_meses.items() if v == filtro_mes][0])]
    return df_filtrado

def graficos(df_filtrado) -> tuple[pd.DataFrame,pd.DataFrame]:
    col1,col2=st.columns(2)
    with col1:     
        df_receitas_e_despesas=df_filtrado.pivot_table(index="Categoria",
                                                       columns="Tipo",
                                                       values="Valor",
                                                       aggfunc="sum",
                                                       fill_value=0).reset_index()
        st.subheader("Total de Receitas e Despesas")
    fig1=px.bar(df_receitas_e_despesas,x="Categoria",y=["receita","despesa"],barmode="stack")
    col1.plotly_chart(fig1)
    with col2:                  
        receitas_mensais=df_filtrado.loc[df_filtrado["Tipo"]=="receita"]
        df_receitas_mensais=receitas_mensais.groupby("Categoria")["Valor"].sum().sort_values(ascending=False)
        df_receitas_mensais=df_receitas_mensais.reset_index()
        st.subheader("Categorias com maiores Receitas")
        if len(df_receitas_mensais)>2:
            df_receitas_mensais=df_receitas_mensais.loc[0:2]
        fig2=px.pie(df_receitas_mensais,names="Categoria",values="Valor")
        col2.plotly_chart(fig2)
    st.divider()
    return df_receitas_e_despesas,df_receitas_mensais

def main():
    upload_planilha=configurar_upload()
    if upload_planilha is not None:
        df,tipo=carregar_dataframe(upload_planilha)
        dict_colunas,colunas_selecionadas=selecionar_colunas(df)
        if colunas_selecionadas==True:
            df_formatado=formatar_colunas(df,dict_colunas)
            df_filtrado=filtrar_df_formatado(df_formatado)
            df_receitas_e_despesas,df_receitas_mensais=graficos(df_filtrado)
if __name__ == "__main__":
    main()
