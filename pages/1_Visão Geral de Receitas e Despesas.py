import streamlit as st
from src.visao_geral.criacao_graficos import agrupar_df_filtrado_para_grafico_receita,agrupar_df_filtrado_para_metricas, gerar_graficos, filtrar_por_ano_mes, criacao_metricas ,grafico_evolucao
from src.visao_geral.criacao_arquivo_excel import criando_arquivo_excel
def main() -> None:
    if "df_formatado" in st.session_state:
        df_formatado=st.session_state.df_formatado

        

        st.title("Visão geral de Receitas e Despesas") 

        tabs = st.tabs(["Resumo do Mês", "Evolução Mensal"])
        with tabs[0]:
            df_filtrado,df_filtrado_anterior,filtro_mes,data_referencia,numero_para_meses=filtrar_por_ano_mes(df_formatado)
            df_receitas_despesas=agrupar_df_filtrado_para_metricas(df_filtrado,filtro_mes)
            df_receitas_despesas_anterior=agrupar_df_filtrado_para_metricas(df_filtrado_anterior,filtro_mes)
            st.subheader(f"Resumo de {filtro_mes}")
            criacao_metricas(df_receitas_despesas,df_receitas_despesas_anterior,filtro_mes)

            df_receitas_mensais=agrupar_df_filtrado_para_grafico_receita(df_filtrado)

            gerar_graficos(df_receitas_despesas,df_receitas_mensais,filtro_mes) 

            st.markdown("### 📄 Exportação do relatório")
            st.markdown("Você pode baixar o relatório financeiro mensal em formato Excel.")
            criando_arquivo_excel(df_receitas_despesas,df_receitas_mensais,data_referencia)
        with tabs[1]:
            grafico_evolucao(df_formatado,numero_para_meses) 

    else:
        st.warning("Faça o upload do arquivo!")
        
if __name__ == "__main__":
    main()
