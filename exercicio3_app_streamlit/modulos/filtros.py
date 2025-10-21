import streamlit as st
import numpy as np

def render(df):
    """Renderiza a página Filtros"""
    st.markdown("# <span style='color: #ff4b4b;'>Filtragem de Dados</span>", unsafe_allow_html=True)

    if df is not None:
        st.markdown("Aplique filtros para explorar subconjuntos dos dados.")

        df_filtrado = df.copy()
        filtros_aplicados = []

        col1, col2 = st.columns(2)

        # Filtro Numérico
        with col1:
            st.markdown("### <span style='color: #ff8c42;'>Filtro Numérico</span>", unsafe_allow_html=True)
            colunas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()

            if len(colunas_numericas) > 0:
                coluna_filtro = st.selectbox(
                    "Selecione a coluna:",
                    colunas_numericas,
                    key='filtro_num_col'
                )

                min_val = float(df[coluna_filtro].min())
                max_val = float(df[coluna_filtro].max())

                valores_range = st.slider(
                    f"Intervalo de {coluna_filtro}:",
                    min_val, max_val, (min_val, max_val),
                    key='filtro_num_range'
                )

                df_filtrado = df_filtrado[
                    (df_filtrado[coluna_filtro] >= valores_range[0]) &
                    (df_filtrado[coluna_filtro] <= valores_range[1])
                ]

                if valores_range != (min_val, max_val):
                    filtros_aplicados.append(f"{coluna_filtro}: {valores_range[0]:.2f} a {valores_range[1]:.2f}")
            else:
                st.info("Nenhuma coluna numérica disponível.")

        # Filtro Categórico
        with col2:
            st.markdown("### <span style='color: #ff8c42;'>Filtro Categórico</span>", unsafe_allow_html=True)
            colunas_categoricas = df.select_dtypes(include=['object', 'category']).columns.tolist()

            if len(colunas_categoricas) > 0:
                coluna_cat = st.selectbox(
                    "Selecione a coluna:",
                    colunas_categoricas,
                    key='filtro_cat_col'
                )

                categorias_unicas = df[coluna_cat].unique().tolist()
                categorias_selecionadas = st.multiselect(
                    f"Selecione as categorias:",
                    categorias_unicas,
                    default=categorias_unicas,
                    key='filtro_cat_vals'
                )

                if len(categorias_selecionadas) > 0:
                    df_filtrado = df_filtrado[df_filtrado[coluna_cat].isin(categorias_selecionadas)]

                if len(categorias_selecionadas) != len(categorias_unicas):
                    filtros_aplicados.append(f"{coluna_cat}: {len(categorias_selecionadas)}/{len(categorias_unicas)} categorias")
            else:
                st.info("Nenhuma coluna categórica disponível.")

        st.divider()

        # Resultado da filtragem
        st.markdown("### <span style='color: #ff8c42;'>Resultado da Filtragem</span>", unsafe_allow_html=True)

        total_original = len(df)
        total_filtrado = len(df_filtrado)
        percentual = (total_filtrado/total_original*100) if total_original > 0 else 0

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Linhas Originais", f"{total_original:,}")
        with col2:
            st.metric("Linhas Filtradas", f"{total_filtrado:,}")
        with col3:
            st.metric("Percentual", f"{percentual:.1f}%")

        if len(filtros_aplicados) > 0:
            st.markdown("**Filtros aplicados:**")
            for filtro in filtros_aplicados:
                st.markdown(f"- {filtro}")
        else:
            st.info("Nenhum filtro aplicado - exibindo todos os dados")

        st.divider()

        # Visualização dos dados filtrados
        st.markdown("### <span style='color: #ff8c42;'>Dados Filtrados</span>", unsafe_allow_html=True)
        st.dataframe(df_filtrado, width='stretch', height=400)

        # Download
        st.divider()
        st.markdown("### <span style='color: #ff8c42;'>Exportar Dados Filtrados</span>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="Download CSV",
                data=df_filtrado.to_csv(index=False).encode('utf-8'),
                file_name='dados_filtrados.csv',
                mime='text/csv'
            )
        with col2:
            st.download_button(
                label="Download Excel",
                data=df_filtrado.to_csv(index=False).encode('utf-8'),
                file_name='dados_filtrados.xlsx',
                mime='application/vnd.ms-excel'
            )
    else:
        st.warning("Nenhum dado carregado. Use a barra lateral para carregar um dataset.")
