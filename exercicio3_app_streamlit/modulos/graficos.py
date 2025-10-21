import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def render(df):
    """Renderiza a página Gráficos"""
    st.markdown("# <span style='color: #ff4b4b;'>Visualizações Interativas</span>", unsafe_allow_html=True)

    if df is not None:
        colunas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()

        if len(colunas_numericas) > 0:
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "Histograma",
                "Dispersão",
                "Box Plot",
                "Correlação",
                "Linha"
            ])

            tema = st.session_state.get('tema_grafico', 'ggplot2')

            # TAB 1: Histograma
            with tab1:
                st.subheader("Histograma - Distribuição de Frequência")

                col1, col2 = st.columns([3, 1])
                with col1:
                    coluna_hist = st.selectbox("Selecione a coluna:", colunas_numericas, key='hist_col')
                with col2:
                    bins = st.slider("Número de bins:", 5, 100, 30, key='hist_bins')

                codigo_hist = f"""import plotly.express as px

fig = px.histogram(
    df,
    x='{coluna_hist}',
    nbins={bins},
    title='Distribuição de {coluna_hist}',
    labels={{'{coluna_hist}': '{coluna_hist}', 'count': 'Frequência'}},
    template='{tema}'
)

fig.update_layout(
    height=500,
    bargap=0.1
)

fig.show()"""

                fig = px.histogram(
                    df,
                    x=coluna_hist,
                    nbins=bins,
                    title=f'Distribuição de {coluna_hist}',
                    labels={coluna_hist: coluna_hist, 'count': 'Frequência'},
                    template=tema
                )

                fig.update_layout(
                    height=500,
                    bargap=0.1
                )

                st.plotly_chart(fig, use_container_width=True)

                with st.expander("Mostrar código-fonte"):
                    st.code(codigo_hist, language='python')

            # TAB 2: Gráfico de Dispersão
            with tab2:
                st.subheader("Gráfico de Dispersão - Relação entre Variáveis")

                col1, col2, col3 = st.columns(3)
                with col1:
                    eixo_x = st.selectbox("Eixo X:", colunas_numericas, key='scatter_x')
                with col2:
                    eixo_y = st.selectbox(
                        "Eixo Y:",
                        colunas_numericas,
                        index=min(1, len(colunas_numericas)-1),
                        key='scatter_y'
                    )
                with col3:
                    colunas_categoricas = df.select_dtypes(include=['object', 'category']).columns.tolist()
                    cor_por = None
                    if len(colunas_categoricas) > 0:
                        usar_cor = st.checkbox("Colorir por categoria", key='scatter_color')
                        if usar_cor:
                            cor_por = st.selectbox("Categoria:", colunas_categoricas, key='scatter_cat')

                cor_param = f"color='{cor_por}'" if cor_por else "color=None"
                codigo_scatter = f"""import plotly.express as px

fig = px.scatter(
    df,
    x='{eixo_x}',
    y='{eixo_y}',
    {cor_param},
    title='{eixo_y} vs {eixo_x}',
    labels={{'{eixo_x}': '{eixo_x}', '{eixo_y}': '{eixo_y}'}},
    template='{tema}'
)

fig.update_layout(height=500)

fig.show()"""

                fig = px.scatter(
                    df,
                    x=eixo_x,
                    y=eixo_y,
                    color=cor_por,
                    title=f'{eixo_y} vs {eixo_x}',
                    labels={eixo_x: eixo_x, eixo_y: eixo_y},
                    template=tema
                )

                fig.update_layout(height=500)

                st.plotly_chart(fig, use_container_width=True)

                with st.expander("Mostrar código-fonte"):
                    st.code(codigo_scatter, language='python')

            # TAB 3: Box Plot
            with tab3:
                st.subheader("Box Plot - Distribuição e Outliers")

                colunas_box = st.multiselect(
                    "Selecione as colunas para comparar:",
                    colunas_numericas,
                    default=colunas_numericas[:min(4, len(colunas_numericas))],
                    key='box_cols'
                )

                if len(colunas_box) > 0:
                    colunas_str = str(colunas_box)
                    codigo_box = f"""import plotly.express as px

# Preparar dados
colunas_selecionadas = {colunas_str}
df_melted = df[colunas_selecionadas].melt(var_name='Coluna', value_name='Valor')

fig = px.box(
    df_melted,
    x='Coluna',
    y='Valor',
    title='Comparação de Distribuições',
    color='Coluna',
    template='{tema}'
)

fig.update_layout(
    height=500,
    showlegend=False
)

fig.show()"""

                    df_melted = df[colunas_box].melt(var_name='Coluna', value_name='Valor')

                    fig = px.box(
                        df_melted,
                        x='Coluna',
                        y='Valor',
                        title='Comparação de Distribuições',
                        color='Coluna',
                        template=tema
                    )

                    fig.update_layout(
                        height=500,
                        showlegend=False
                    )

                    st.plotly_chart(fig, use_container_width=True)

                    with st.expander("Mostrar código-fonte"):
                        st.code(codigo_box, language='python')
                else:
                    st.info("Selecione pelo menos uma coluna para visualizar.")

            # TAB 4: Matriz de Correlação
            with tab4:
                st.subheader("Matriz de Correlação")

                if len(colunas_numericas) > 1:
                    colunas_num_str = str(colunas_numericas)
                    codigo_corr = f"""import plotly.express as px

# Calcular correlação
colunas_numericas = {colunas_num_str}
corr = df[colunas_numericas].corr()

fig = px.imshow(
    corr,
    text_auto='.2f',
    aspect='auto',
    color_continuous_scale='RdBu_r',
    color_continuous_midpoint=0,
    title='Matriz de Correlação entre Variáveis',
    template='{tema}'
)

fig.update_layout(height=600)

fig.show()"""

                    corr = df[colunas_numericas].corr()

                    fig = px.imshow(
                        corr,
                        text_auto='.2f',
                        aspect='auto',
                        color_continuous_scale='RdBu_r',
                        color_continuous_midpoint=0,
                        title='Matriz de Correlação entre Variáveis',
                        template=tema
                    )

                    fig.update_layout(height=600)

                    st.plotly_chart(fig, use_container_width=True)

                    with st.expander("Mostrar código-fonte"):
                        st.code(codigo_corr, language='python')

                    st.divider()
                    st.subheader("Top 10 Correlações Mais Fortes")

                    # Extrair correlações
                    corr_pairs = corr.unstack()
                    corr_pairs = corr_pairs[corr_pairs < 1]  # Remove autocorrelação
                    corr_pairs = corr_pairs.abs().sort_values(ascending=False).drop_duplicates()

                    top_corr = pd.DataFrame({
                        'Par de Variáveis': [f"{idx[0]} - {idx[1]}" for idx in corr_pairs.head(10).index],
                        'Correlação': corr_pairs.head(10).values
                    })

                    st.dataframe(top_corr, width='stretch', hide_index=True)
                else:
                    st.info("Necessário pelo menos duas colunas numéricas para calcular correlações.")

            # TAB 5: Gráfico de Linha
            with tab5:
                st.subheader("Gráfico de Linha - Tendências")

                col1, col2 = st.columns(2)
                with col1:
                    colunas_linha = st.multiselect(
                        "Selecione as colunas para plotar:",
                        colunas_numericas,
                        default=colunas_numericas[:min(3, len(colunas_numericas))],
                        key='line_cols'
                    )
                with col2:
                    limite_linhas = st.slider(
                        "Número de pontos a exibir:",
                        10, len(df), min(100, len(df)),
                        key='line_limit'
                    )

                if len(colunas_linha) > 0:
                    colunas_linha_str = str(colunas_linha)
                    codigo_linha = f"""import plotly.graph_objects as go

# Preparar dados
colunas_selecionadas = {colunas_linha_str}
df_plot = df[colunas_selecionadas].head({limite_linhas})

fig = go.Figure()

for col in colunas_selecionadas:
    fig.add_trace(go.Scatter(
        y=df_plot[col],
        mode='lines+markers',
        name=col,
        line=dict(width=2),
        marker=dict(size=6)
    ))

fig.update_layout(
    template='{tema}',
    height=500,
    title="Evolução das Variáveis",
    hovermode='x unified',
    xaxis_title="Índice",
    yaxis_title="Valor"
)

fig.show()"""

                    df_plot = df[colunas_linha].head(limite_linhas)

                    fig = go.Figure()

                    for col in colunas_linha:
                        fig.add_trace(go.Scatter(
                            y=df_plot[col],
                            mode='lines+markers',
                            name=col,
                            line=dict(width=2),
                            marker=dict(size=6)
                        ))

                    fig.update_layout(
                        template=tema,
                        height=500,
                        title="Evolução das Variáveis",
                        hovermode='x unified',
                        xaxis_title="Índice",
                        yaxis_title="Valor"
                    )

                    st.plotly_chart(fig, use_container_width=True)

                    with st.expander("Mostrar código-fonte"):
                        st.code(codigo_linha, language='python')
                else:
                    st.info("Selecione pelo menos uma coluna para visualizar.")
        else:
            st.warning("Nenhuma coluna numérica encontrada no dataset.")
    else:
        st.warning("Nenhum dado carregado. Use a barra lateral para carregar um dataset.")
