from src.visao_geral.criacao_graficos import agrupar_df,gerar_graficos,filtrar_por_ano_mes,criacao_metricas
from src.visao_geral.criacao_arquivo_excel import criando_arquivo_excel
import streamlit as st

def main() -> None:
    if "df_formatado" in st.session_state:
        df_formatado=st.session_state.df_formatado
        st.title("Visão geral de Receitas e Despesas")
        df_filtrado,df_filtrado_anterior,filtro_mes,data_referencia=filtrar_por_ano_mes(df_formatado)

        df_receitas_despesas=df_filtrado=agrupar_df(df_filtrado,filtro_mes)
        df_receitas_despesas_anterior=df_filtrado_anterior=agrupar_df(df_filtrado_anterior,filtro_mes)

        criacao_metricas(df_receitas_despesas,df_receitas_despesas_anterior)
        gerar_graficos(df_receitas_despesas) 
        # criando_arquivo_excel(df_receitas_despesas,df_receitas_mensais,data_referencia)
    else:
        st.warning("Faça o upload do arquivo!")
        
if __name__ == "__main__":
    main()
