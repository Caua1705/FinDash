import streamlit as st
from src.visao_geral.criacao_graficos import agrupar_dados_para_grafico_receita,agrupar_dados_para_metricas, exibir_graficos_receitas_despesas, filtrar_dados_por_ano_mes, exibir_metricas_financeiras ,exibir_evolucao_mensal
from src.visao_geral.criacao_arquivo_excel import gerar_arquivo_excel
def main() -> None:
    if "df_formatado" in st.session_state:
        df_formatado=st.session_state.df_formatado
        st.title("Visão geral de Receitas e Despesas") 
        
        df_filtrado,df_filtrado_anterior,filtro_mes,data_referencia,numero_para_meses=filtrar_dados_por_ano_mes(df_formatado)

        df_receitas_despesas=agrupar_dados_para_metricas(df_filtrado)
        df_receitas_despesas_anterior=agrupar_dados_para_metricas(df_filtrado_anterior)

        exibir_metricas_financeiras(df_receitas_despesas,df_receitas_despesas_anterior)

        tabs = st.tabs(["Resumo do Mês", "Evolução Mensal"])
        with tabs[0]:

            df_receitas_mensais=agrupar_dados_para_grafico_receita(df_filtrado)
            exibir_graficos_receitas_despesas(df_receitas_despesas,df_receitas_mensais,filtro_mes) 

            st.markdown("### 📄 Exportação do relatório")
            st.markdown("Você pode baixar o relatório financeiro mensal em formato Excel.")
            gerar_arquivo_excel(df_receitas_despesas,df_receitas_mensais,data_referencia)

        with tabs[1]:
            exibir_evolucao_mensal(df_formatado,numero_para_meses) 

    else:
        st.warning("Faça o upload do arquivo!")
        
if __name__ == "__main__":
    main()
