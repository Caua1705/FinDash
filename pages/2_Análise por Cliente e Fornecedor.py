import streamlit as st
from src.analise_clientes.criacao_graficos import filtrar_dataframes_para_graficos,gerar_graficos

def main() -> None:
    if "df_formatado" in st.session_state:
        df_formatado=st.session_state.df_formatado
        st.title("Análise por Cliente e Fornecedor")
        try:
            data_inicial=st.sidebar.date_input("Data Inicial")
            data_final=st.sidebar.date_input("Data Final")
        except KeyError:
            st.warning("Não há valores para essa data.")
        df_filtrado=df_formatado.loc[(df_formatado["Data"].dt.date >= data_inicial ) & (df_formatado["Data"].dt.date <= data_final )]
        df_clientes=df_filtrado[df_filtrado["Tipo"]=="Receitas"]
        df_fornecedores=df_filtrado[df_filtrado["Tipo"]=="Despesas"]
        df_filtrado_clientes=filtrar_dataframes_para_graficos(df_clientes)
        df_filtrado_fornecedores=filtrar_dataframes_para_graficos(df_fornecedores)
        gerar_graficos(df_filtrado_clientes,df_filtrado_fornecedores)

    else:
        st.warning("Faça o upload do arquivo!")
        
if __name__ == "__main__":
    main()

