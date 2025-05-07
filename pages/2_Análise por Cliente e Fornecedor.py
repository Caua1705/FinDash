import streamlit as st

#Processamento de Dados
from analise_clientes.processamento_dados.filtrar_dados import selecionar_data,filtrar_dados_data,selecionar_clientes_fornecedores
from analise_clientes.processamento_dados.agrupar_dados import agrupar_dados

#Métricas
from analise_clientes.metricas.exibir_metricas import criar_metricas

#Gráficos
from analise_clientes.graficos.principais_clientes import exibir_grafico_principais_clientes
from analise_clientes.graficos.principais_fornecedores import exibir_grafico_principais_fornecedores

#Transações Detalhadas
from analise_clientes.transaçoes_detalhadas.transacoes import exibir_transacoes

def main() -> None:
    if "df_formatado" in st.session_state:
        df_formatado=st.session_state.df_formatado
        st.title("Análise por Cliente e Fornecedor")
        st.write(df_formatado)

        #Filtragem de dados por data selecionada
        data_inicial,data_final=selecionar_data()
        df_filtrado=filtrar_dados_data(df_formatado,data_inicial,data_final)
        df_clientes,df_fornecedores=selecionar_clientes_fornecedores(df_filtrado)

        #Agrupar dados
        df_agrupado_clientes=agrupar_dados(df_clientes)
        df_agrupado_fornecedores=agrupar_dados(df_fornecedores)

        #Exibir Métricas
        criar_metricas(df_agrupado_clientes,df_agrupado_fornecedores)

        tabs = st.tabs(["Gráficos", "Transações Detalhadas"])
      
        with tabs[0]:
            #Gráficos: Principais Clientes + Principais Fornecedores
            exibir_grafico_principais_clientes(df_agrupado_clientes)
            exibir_grafico_principais_fornecedores(df_agrupado_fornecedores)

        with tabs[1]:
            st.markdown("### Detalhamento das Transações")
            #Exibir Transações Detalhadas 
            exibir_transacoes(df_filtrado)

    else:
        st.warning("Faça o upload do arquivo!")
        
if __name__ == "__main__":
    main()

