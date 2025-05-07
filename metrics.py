import streamlit as st
import pandas as pd
import ast
import re

st.title("Editor de Grupos de Métricas do App")

# Upload do código-fonte do app
code_file = st.file_uploader("Carregar código do app (.py)", type=["py"])
xls_file = st.file_uploader("Carregar template de métricas (.xlsx)", type=["xlsx"])

if code_file and xls_file:
    # Leitura dos arquivos
    code_text = code_file.read().decode("utf-8")
    df_template = pd.read_excel(xls_file)

    # Lista todas as colunas disponíveis no arquivo Excel
    all_metrics = list(df_template.columns)
    st.subheader("Criar novo grupo de métricas")
    group_name = st.text_input("Nome do novo grupo")
    selected_metrics = st.multiselect("Selecionar métricas para o grupo", all_metrics)

    if st.button("Inserir grupo no código"):
        # Busca a definição atual de pizza_selected_groups
        match = re.search(r"pizza_selected_groups\s*=\s*({.*?})", code_text, re.DOTALL)
        if not match:
            st.error("Não foi possível localizar a variável 'pizza_selected_groups' no código.")
        else:
            try:
                # Converte o dicionário atual para Python
                groups_dict = ast.literal_eval(match.group(1))
                groups_dict[group_name] = selected_metrics  # Adiciona novo grupo

                # Constrói a nova definição como string
                new_dict_str = "pizza_selected_groups = " + repr(groups_dict)

                # Substitui o trecho antigo no código
                new_code = re.sub(
                    r"pizza_selected_groups\s*=\s*{.*?}",
                    new_dict_str,
                    code_text,
                    flags=re.DOTALL
                )

                # Sucesso e download
                st.success(f"Grupo '{group_name}' adicionado com sucesso!")
                st.download_button(
                    label="Baixar novo código do app",
                    data=new_code,
                    file_name="novo_app.py",
                    mime="text/x-python"
                )
            except Exception as e:
                st.error(f"Erro ao modificar o código: {e}")
