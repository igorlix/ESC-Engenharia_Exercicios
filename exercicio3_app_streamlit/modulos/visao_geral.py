import streamlit as st
import pandas as pd

def render(df):
    """Renderiza a página Visão Geral"""
    st.markdown("# <span style='color: #ff4b4b;'>Visão Geral dos Dados</span>", unsafe_allow_html=True)

    if df is not None:
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Linhas", f"{df.shape[0]:,}")
        with col2:
            st.metric("Colunas", f"{df.shape[1]}")
        with col3:
            st.metric("Tamanho (KB)", f"{df.memory_usage(deep=True).sum() / 1024:.2f}")
        with col4:
            st.metric("Valores Nulos", f"{df.isnull().sum().sum()}")

        st.divider()

        # Prévia dos dados
        st.markdown("### <span style='color: #ff8c42;'>Prévia dos Dados</span>", unsafe_allow_html=True)
        num_linhas = st.slider("Número de linhas a exibir:", 5, 50, 10)
        st.dataframe(df.head(num_linhas), width='stretch', height=400)

        st.divider()

        # Informações das colunas
        st.markdown("### <span style='color: #ff8c42;'>Informações das Colunas</span>", unsafe_allow_html=True)

        info_df = pd.DataFrame({
            'Coluna': df.columns,
            'Tipo': [str(dtype) for dtype in df.dtypes.values],
            'Não-Nulos': df.count().values,
            'Nulos': df.isnull().sum().values,
            '% Nulos': (df.isnull().sum() / len(df) * 100).values
        })

        st.dataframe(info_df, width='stretch', hide_index=True)

        # Download dos dados
        st.divider()
        st.markdown("### <span style='color: #ff8c42;'>Download dos Dados</span>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="Baixar como CSV",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name='dados_completos.csv',
                mime='text/csv'
            )
        with col2:
            st.download_button(
                label="Baixar como Excel",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name='dados_completos.xlsx',
                mime='application/vnd.ms-excel'
            )
    else:
        st.warning("Nenhum dado carregado. Use a barra lateral para carregar um dataset.")
