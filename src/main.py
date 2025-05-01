from processamento_dados import carregar_arquivo,carregar_dataframe,selecionar_colunas_dataframe,formatar_colunas_dataframe,filtrar_df_formatado_por_ano_mes
from criacao_graficos import filtrar_dataframes_para_graficos,gerar_graficos
from criacao_arquivo_excel import criando_arquivo_excel

def main() -> None:
    upload_planilha=carregar_arquivo()
    if upload_planilha is not None:
        df=carregar_dataframe(upload_planilha)
        dict_colunas=selecionar_colunas_dataframe(df)
        df_formatado=formatar_colunas_dataframe(df,dict_colunas)
        df_filtrado,filtro_mes,data_referencia=filtrar_df_formatado_por_ano_mes(df_formatado)
        df_receitas_despesas,df_receitas_mensais=filtrar_dataframes_para_graficos(df_filtrado)
        gerar_graficos(df_receitas_despesas,df_receitas_mensais,filtro_mes)
        criando_arquivo_excel(df_receitas_despesas,df_receitas_mensais,data_referencia)
        
if __name__ == "__main__":
    main()
