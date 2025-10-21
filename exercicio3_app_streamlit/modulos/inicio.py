import streamlit as st
import numpy as np

def render(df):
    """Renderiza a página Início"""
    st.markdown("# <span style='color: #ff4b4b;'>Aplicação de Análise de Dados</span>", unsafe_allow_html=True)
    st.markdown("Plataforma para análise exploratória de dados com visualizações interativas.")

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### <span style='color: #ff8c42;'>Objetivo</span>", unsafe_allow_html=True)
        st.write("Ferramenta para análise exploratória de dados com visualizações interativas e estatísticas descritivas.")

    with col2:
        st.markdown("### <span style='color: #ff8c42;'>Recursos</span>", unsafe_allow_html=True)
        st.write("Upload de CSV/Excel")
        st.write("Estatísticas descritivas")
        st.write("Múltiplos gráficos")
        st.write("Filtros de dados")

    with col3:
        st.markdown("### <span style='color: #ff8c42;'>Como Usar</span>", unsafe_allow_html=True)
        st.write("1. Carregue seus dados")
        st.write("2. Navegue pelas páginas")
        st.write("3. Analise e filtre")
        st.write("4. Exporte resultados")

    if df is not None:
        st.divider()
        st.markdown("### <span style='color: #ff8c42;'>Dados Carregados</span>", unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total de Linhas", f"{df.shape[0]:,}")
        with col2:
            st.metric("Total de Colunas", f"{df.shape[1]}")
        with col3:
            st.metric("Colunas Numéricas", f"{len(df.select_dtypes(include=[np.number]).columns)}")
        with col4:
            st.metric("Valores Nulos", f"{df.isnull().sum().sum()}")

        st.info("Use o menu lateral para navegar entre as páginas.")
    else:
        st.info("Carregue um dataset na barra lateral para começar a análise.")
