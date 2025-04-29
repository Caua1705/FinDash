import pandas as pd
import streamlit as st
import plotly.express as px
from jinja2 import FileSystemLoader,Environment
from pathlib import Path
from datetime import datetime
import tempfile
from openpyxl import load_workbook

def carregar_arquivo():
    st.set_page_config(page_title="FinDash",layout="wide",page_icon="💲") 
    st.title("Planilha Financeira:")
    st.write("Escolha um arquivo do tipo CSV ou XLSX para carregar a planilha:")
    upload_planilha=st.file_uploader("Selecione o arquivo:",accept_multiple_files=False,type=["xlsx","csv"])
    return upload_planilha

def carregar_dataframe(arquivo) -> tuple[pd.DataFrame,str]:
    if arquivo.name.endswith("xlsx"):
        df=pd.read_excel(arquivo)
    if arquivo.name.endswith("csv"):
        df=pd.read_csv(arquivo)
    return df

def selecionar_colunas_dataframe(df) -> tuple[dict[str,str], bool]:
    columns=st.sidebar
    columns.write("### Seleção de Colunas:")
    coluna_data=columns.selectbox("Selecione a coluna Data(dd/mm/yyyy)",list(df.columns),help="Coluna onde está a data da transação")
    coluna_categoria=columns.selectbox("Selecione a coluna Categoria",[a for a in list(df.columns) if a != coluna_data],help="Coluna onde está a Categoria da transação")
    coluna_tipo=columns.selectbox("Selecione a coluna Tipo(Receita/Despesa)",[a for a in list(df.columns) if a != coluna_data and a != coluna_categoria],help="Coluna onde está a tipo da transação")
    coluna_valor=columns.selectbox("Selecione a coluna Valor",[a for a in list(df.columns) if a != coluna_data and a != coluna_categoria and a != coluna_tipo],help="Coluna onde está o valor da transação")
    if "colunas_selecionadas" not in st.session_state:
        st.session_state.colunas_selecionadas=False
    if columns.button("Visualizar Dashboard"):
        st.session_state.colunas_selecionadas=True
    dict_colunas={"Data":coluna_data,
                  "Categoria":coluna_categoria, 
                  "Tipo":coluna_tipo,
                  "Valor":coluna_valor}
    return dict_colunas,st.session_state.colunas_selecionadas

def formatar_colunas_dataframe(df,colunas_dataframe) -> pd.DataFrame:
    df_formatado=df.copy()
    df_formatado=df_formatado.rename(columns={colunas_dataframe["Data"] :"Data",
                                      colunas_dataframe["Categoria"] :"Categoria",
                                      colunas_dataframe["Tipo"] : "Tipo",
                                      colunas_dataframe["Valor"] : "Valor"
                                      })
    formatacao_letras_tipo=df_formatado["Tipo"].str.lower()
    coluna_formatada=pd.to_datetime(df_formatado["Data"],dayfirst=True) #Formata a coluna data do DataFrame
    df_formatado["Tipo"]=formatacao_letras_tipo
    df_formatado["Data"]=coluna_formatada
    return df_formatado

def filtrar_df_formatado(df_formatado) -> tuple[pd.DataFrame,str]:
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
        data_filtrada=df_filtrado["Data"].iloc[0]
        data_referencia=data_filtrada.strftime("%Y-%m")
    return df_filtrado,filtro_mes,data_referencia

def gerar_dataframes_para_graficos(df_filtrado) ->tuple[pd.DataFrame,pd.DataFrame]:
    df_receitas_despesas=df_filtrado.pivot_table(index="Categoria",
                                                       columns="Tipo",
                                                       values="Valor",
                                                       aggfunc="sum",
                                                       fill_value=0,
                                                       )
    df_receitas_despesas=df_receitas_despesas.rename(columns={"receita":"Receitas",
                                                                "despesa":"Despesas"}).reset_index()
    df_receitas_despesas=df_receitas_despesas[["Categoria","Receitas","Despesas"]]
    df_receitas_despesas=df_receitas_despesas.sort_values(by="Receitas",ascending=False)
    df_receitas_despesas.columns.name=None
    df_receitas_despesas.loc[len(df_receitas_despesas)] = ["TOTAL",
                                                           df_receitas_despesas["Receitas"].sum()
                                                           ,df_receitas_despesas["Despesas"].sum()]
    receitas_mensais=df_filtrado.loc[df_filtrado["Tipo"]=="receita"]
    df_receitas_mensais=receitas_mensais.groupby("Categoria")["Valor"].sum().sort_values(ascending=False)
    df_receitas_mensais=df_receitas_mensais.reset_index()
    return df_receitas_despesas,df_receitas_mensais

def gerar_graficos(df_receitas_despesas,df_receitas_mensais) -> None:
    col1,col2=st.columns(2)
    with col1:    
        st.subheader("Total de Receitas e Despesas")
        fig1=px.bar(df_receitas_despesas,x="Categoria",y=["Receitas","Despesas"],barmode="group",labels={"Categoria": "Categoria", "valor": "Valor"},title="Receitas e Despesas por Categoria")
        fig1.update_layout(xaxis_tickangle=-45,xaxis_title="Categoria",yaxis_title="Valor",showlegend=True)
        col1.plotly_chart(fig1)
    with col2:                  
        st.subheader("Categorias com maiores Receitas")
        if len(df_receitas_mensais)>2:
            df_receitas_mensais=df_receitas_mensais.loc[0:2]
        fig2=px.pie(df_receitas_mensais,names="Categoria",values="Valor",title="Distribuição das maiores Receitas",color="Categoria")
        fig2.update_traces(textinfo="percent+label")       
        col2.plotly_chart(fig2)
    st.divider() 

def formatar_para_excel(df_receitas_despesas,df_receitas_mensais,data_referencia):
    with tempfile.TemporaryDirectory() as dir_temp:
        nome_arquivo=f"Relatório mensal - {data_referencia}.xlsx"
        diretorio_arquivo_temporario= Path(dir_temp) / nome_arquivo

        with pd.ExcelWriter(diretorio_arquivo_temporario) as escritor:
            df_receitas_despesas.to_excel(escritor,sheet_name="Receitas e Despesas",index=False)
            df_receitas_mensais.to_excel(escritor,sheet_name="Receitas Mensais",index=False)

        # wb=load_workbook(diretorio_arquivo_temporario)
        with open(diretorio_arquivo_temporario,"rb") as leitor:
            arquivo=leitor.read()
            botao_download=st.sidebar.download_button("Clique para fazer o download do arquivo",
                                                     data=arquivo,
                                                     file_name=nome_arquivo,
                                                     mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    return arquivo


def main():
    upload_planilha=carregar_arquivo()
    if upload_planilha is not None:
        df=carregar_dataframe(upload_planilha)
        dict_colunas,colunas_selecionadas=selecionar_colunas_dataframe(df)
        if colunas_selecionadas==True:
            df_formatado=formatar_colunas_dataframe(df,dict_colunas)
            df_filtrado,filtro_mes,data_referencia=filtrar_df_formatado(df_formatado)
            df_receitas_despesas,df_receitas_mensais=gerar_dataframes_para_graficos(df_filtrado)
            gerar_graficos(df_receitas_despesas,df_receitas_mensais)
            arquivo=formatar_para_excel(df_receitas_despesas,df_receitas_mensais,data_referencia)
    else:
        st.session_state.pop("colunas_selecionadas", None)

if __name__ == "__main__":
    main()
