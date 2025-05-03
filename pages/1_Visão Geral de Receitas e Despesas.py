from src.visao_geral.criacao_graficos import filtrar_dataframes_para_graficos,gerar_graficos,filtrar_df_formatado_por_ano_mes
from src.visao_geral.criacao_arquivo_excel import criando_arquivo_excel
import streamlit as st

def main() -> None:
    if "df_formatado" in st.session_state:
        df_formatado=st.session_state.df_formatado
        st.title("Visão geral de Receitas e Despesas")
        df_filtrado,filtro_mes,data_referencia=filtrar_df_formatado_por_ano_mes(df_formatado)
        df_receitas_despesas,df_receitas_mensais=filtrar_dataframes_para_graficos(df_filtrado,filtro_mes)
        gerar_graficos(df_receitas_despesas,df_receitas_mensais,filtro_mes)
        criando_arquivo_excel(df_receitas_despesas,df_receitas_mensais,data_referencia)
    else:
        st.warning("Faça o upload do arquivo!")
        
if __name__ == "__main__":
    main()
