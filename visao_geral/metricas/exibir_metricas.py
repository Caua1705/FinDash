import streamlit as st

def exibir_metricas_financeiras(df_receitas_despesas,df_receitas_despesas_anterior):
    df_receitas_despesas=df_receitas_despesas.loc[df_receitas_despesas["Centro de Custo / Receita"]!="TOTAL"]
    col1,col2,col3,col4=st.columns(4)

    with col1:
        total_receitas=df_receitas_despesas["Receitas"].sum()
        total_receitas_anterior=df_receitas_despesas_anterior["Receitas"].sum() if not df_receitas_despesas_anterior.empty else 0
        delta_receitas=(total_receitas-total_receitas_anterior) / total_receitas_anterior * 100 if not df_receitas_despesas_anterior.empty else 0
        st.metric("Receita Total",f"R$ {total_receitas:,.2f}",f"{delta_receitas:.2f}%",delta_color="normal")

    with col2:
        total_despesas=df_receitas_despesas["Despesas"].sum()
        total_despesas_anterior=df_receitas_despesas_anterior["Despesas"].sum() if not df_receitas_despesas_anterior.empty else 0
        delta_despesas=(total_despesas_anterior-total_despesas) / total_despesas_anterior * 100 if not df_receitas_despesas_anterior.empty else 0
        st.metric("Despesa Total",f"R$ {total_despesas:,.2f}",f"{delta_despesas:.2f}%",delta_color="inverse")

    with col3:
        saldo_liquido=total_receitas-total_despesas
        saldo_liquido_anterior=total_receitas_anterior-total_despesas_anterior if not df_receitas_despesas_anterior.empty else 0
        delta_saldo=(saldo_liquido-saldo_liquido_anterior) / saldo_liquido_anterior * 100 if not df_receitas_despesas_anterior.empty else 0
        st.metric("Saldo Líquido",f"R$ {saldo_liquido:,.2f}",f"{delta_saldo:.2f}%",delta_color="normal")
        
    with col4:
        roi_consolidado=(saldo_liquido/total_despesas) * 100
        roi_consolidado_anterior=(saldo_liquido_anterior/total_despesas_anterior) * 100 if not df_receitas_despesas_anterior.empty else 0
        delta_roi= (roi_consolidado - roi_consolidado_anterior) / roi_consolidado_anterior * 100 if not df_receitas_despesas_anterior.empty else 0
        st.metric("ROI Consolidado",f"{roi_consolidado:,.2f}%",f"{delta_roi:.2f}%")