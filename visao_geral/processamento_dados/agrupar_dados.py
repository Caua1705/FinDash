import pandas as pd

def agrupar_receitas_despesas(df_filtrado) -> pd.DataFrame:
    df_receitas_despesas=df_filtrado.pivot_table(index=["Centro de Custo / Receita"],
                                                    columns="Tipo",
                                                    values="Valor",
                                                    aggfunc="sum",
                                                    fill_value=0,
                                                    ).reset_index()
    if not df_receitas_despesas.empty:
        df_receitas_despesas=df_receitas_despesas[["Centro de Custo / Receita","Receitas","Despesas"]]
        df_receitas_despesas=df_receitas_despesas.sort_values(by="Receitas",ascending=False)
        df_receitas_despesas.loc[len(df_receitas_despesas)] = ["TOTAL",df_receitas_despesas["Receitas"].sum(),
                                                            df_receitas_despesas["Despesas"].sum()]
    return df_receitas_despesas

def agrupar_principais_receitas(df_filtrado):
    receitas_mensais=df_filtrado.loc[df_filtrado["Tipo"]=="Receitas"]
    df_receitas_mensais=receitas_mensais.groupby("Centro de Custo / Receita")["Valor"].sum().sort_values(ascending=False).reset_index()
    df_receitas_mensais.loc[len(df_receitas_mensais)] = ["TOTAL",df_receitas_mensais["Valor"].sum()]
    if len(df_receitas_mensais)>2:
            df_receitas_mensais=df_receitas_mensais.loc[0:2]
    return df_receitas_mensais

def agrupar_evolucao_mensal(df_formatado,numero_para_meses):
    df_formatado["Mês"]=df_formatado["Data"].dt.month
    df_evolucao_mensal=df_formatado.groupby(["Mês","Tipo"])["Valor"].sum().reset_index()
    df_evolucao_mensal["Mês"]=df_evolucao_mensal["Mês"].apply(lambda x: numero_para_meses[x] if x in numero_para_meses else x)
    return df_evolucao_mensal
