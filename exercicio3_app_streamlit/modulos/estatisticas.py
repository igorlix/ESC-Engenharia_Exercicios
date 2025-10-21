import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def render(df):
    """Renderiza a página Estatísticas"""
    st.markdown("# <span style='color: #ff4b4b;'>Estatísticas Descritivas</span>", unsafe_allow_html=True)

    if df is not None:
        colunas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()

        if len(colunas_numericas) > 0:
            # Resumo estatístico completo
            st.markdown("### <span style='color: #ff8c42;'>Resumo Estatístico Completo</span>", unsafe_allow_html=True)
            st.dataframe(df[colunas_numericas].describe(), width='stretch')

            st.divider()

            # Análise detalhada por coluna
            st.markdown("### <span style='color: #ff8c42;'>Análise Detalhada por Coluna</span>", unsafe_allow_html=True)
            coluna_selecionada = st.selectbox(
                "Selecione uma coluna para análise detalhada:",
                colunas_numericas
            )

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Média", f"{df[coluna_selecionada].mean():.4f}")
            with col2:
                st.metric("Mediana", f"{df[coluna_selecionada].median():.4f}")
            with col3:
                moda_val = df[coluna_selecionada].mode()
                moda_str = f"{moda_val[0]:.4f}" if len(moda_val) > 0 else "N/A"
                st.metric("Moda", moda_str)
            with col4:
                st.metric("Desvio Padrão", f"{df[coluna_selecionada].std():.4f}")

            col5, col6, col7, col8 = st.columns(4)
            with col5:
                st.metric("Mínimo", f"{df[coluna_selecionada].min():.4f}")
            with col6:
                st.metric("Máximo", f"{df[coluna_selecionada].max():.4f}")
            with col7:
                st.metric("Q1 (25%)", f"{df[coluna_selecionada].quantile(0.25):.4f}")
            with col8:
                st.metric("Q3 (75%)", f"{df[coluna_selecionada].quantile(0.75):.4f}")

            st.divider()

            col9, col10, col11, col12 = st.columns(4)
            with col9:
                st.metric("Variância", f"{df[coluna_selecionada].var():.4f}")
            with col10:
                iqr = df[coluna_selecionada].quantile(0.75) - df[coluna_selecionada].quantile(0.25)
                st.metric("IQR", f"{iqr:.4f}")
            with col11:
                st.metric("Assimetria", f"{df[coluna_selecionada].skew():.4f}")
            with col12:
                st.metric("Curtose", f"{df[coluna_selecionada].kurtosis():.4f}")

            # Visualização da distribuição
            st.divider()
            st.subheader(f"Distribuição de {coluna_selecionada}")

            tema_atual = st.session_state.get('tema_grafico', 'ggplot2')

            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=df[coluna_selecionada],
                name='Distribuição',
                marker_color='steelblue',
                opacity=0.7
            ))

            fig.update_layout(
                template=tema_atual,
                height=400,
                xaxis_title=coluna_selecionada,
                yaxis_title="Frequência",
                showlegend=False,
                bargap=0.1
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("Nenhuma coluna numérica encontrada no dataset.")
    else:
        st.warning("Nenhum dado carregado. Use a barra lateral para carregar um dataset.")
