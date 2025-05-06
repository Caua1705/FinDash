import streamlit as st
from src.analise_clientes.tela_principal import filtrar_dataframes_para_graficos,gerar_graficos,criar_metricas,transacoes_detalhadas

def main() -> None:
    if "df_formatado" in st.session_state:
        df_formatado=st.session_state.df_formatado
        st.title("Análise por Cliente e Fornecedor")

        data_inicial=st.sidebar.date_input("Data Inicial")
        data_final=st.sidebar.date_input("Data Final")
        if data_inicial>data_final:
            st.error("A data inicial não pode ser maior que a data final")
        df_filtrado=df_formatado.loc[(df_formatado["Data"].dt.date >= data_inicial ) & (df_formatado["Data"].dt.date <= data_final )]

        df_clientes=df_filtrado[df_filtrado["Tipo"]=="Receitas"]
        df_fornecedores=df_filtrado[df_filtrado["Tipo"]=="Despesas"]
        
        df_filtrado_clientes=filtrar_dataframes_para_graficos(df_clientes)
        df_filtrado_fornecedores=filtrar_dataframes_para_graficos(df_fornecedores)

        criar_metricas(df_filtrado_clientes,df_filtrado_fornecedores)

        tabs = st.tabs(["Gráficos", "Transações Detalhadas"])
        with tabs[0]:
            gerar_graficos(df_filtrado_clientes,df_filtrado_fornecedores)
        with tabs[1]:
            st.markdown("### Detalhamento das Transações")
            transacoes_detalhadas(df_filtrado)

    else:
        st.warning("Faça o upload do arquivo!")
        
if __name__ == "__main__":
    main()

