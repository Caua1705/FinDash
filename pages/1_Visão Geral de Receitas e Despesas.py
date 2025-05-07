import streamlit as st

#Processamento de Dados
from visao_geral.processamento_dados.filtrar_dados import obter_filtros_ano_mes,filtrar_dados_ano_mes
from visao_geral.processamento_dados.agrupar_dados import agrupar_receitas_despesas,agrupar_principais_receitas,agrupar_evolucao_mensal

#Métricas
from visao_geral.metricas.exibir_metricas import exibir_metricas_financeiras

#Gráficos
from visao_geral.graficos.receitas_despesas import exibir_grafico_receitas_despesas
from visao_geral.graficos.principais_receitas import exibir_grafico_principais_receitas
from visao_geral.graficos.evolucao_mensal import exibir_grafico_evolucao_mensal

#Exportação
from visao_geral.exportar.criacao_arquivo_excel import gerar_arquivo_excel

def main() -> None:
    if "df_formatado" in st.session_state:
        df_formatado=st.session_state.df_formatado
        st.title("Visão geral de Receitas e Despesas") 

        #Filtragem de dados por ano e mês selecionados
        filtros=obter_filtros_ano_mes(df_formatado)
        df_filtrado,df_filtrado_anterior=filtrar_dados_ano_mes(df_formatado,
                                                                filtros["ano_escolhido"],
                                                                filtros["mes_escolhido_numero"])

        #Agrupar Dados
        df_receitas_despesas=agrupar_receitas_despesas(df_filtrado)
        df_receitas_despesas_anterior=agrupar_receitas_despesas(df_filtrado_anterior)
        df_receitas_mensais=agrupar_principais_receitas(df_filtrado)
        df_evolucao_mensal=agrupar_evolucao_mensal(df_formatado,filtros["numero_para_meses"])

        #Exibir Métricas
        exibir_metricas_financeiras(df_receitas_despesas,df_receitas_despesas_anterior)

        tabs = st.tabs(["Resumo do Mês", "  Evolução Mensal"])

        with tabs[0]:   

            # Gráficos: Total de Receitas e Despesas + Principais Categorias de Receita
            col1,col2=st.columns(2)
            with col1:
                exibir_grafico_receitas_despesas(df_receitas_despesas,filtros["mes_escolhido_nome"])
            with col2:
                exibir_grafico_principais_receitas(df_receitas_mensais,filtros["mes_escolhido_nome"])
            st.divider()

            #Exportação do relatório para Excel
            st.markdown("### 📄 Exportação do relatório")
            st.markdown("Você pode baixar o relatório financeiro mensal em formato Excel.")
            gerar_arquivo_excel(df_receitas_despesas,df_receitas_mensais,filtros["data_formatada"])
            st.divider()
            st.caption("Desenvolvido por Cauã de Carvalho Oliveira Peixoto - Todos os direitos reservados © 2025")

        with tabs[1]:
            #Exibir gráfico de Evolução mensal 
            exibir_grafico_evolucao_mensal(df_evolucao_mensal)

    else:
        st.warning("Faça o upload do arquivo!")
        
if __name__ == "__main__":
    main()
