import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.datasets import load_iris, fetch_california_housing

st.set_page_config(page_title="Análise de Dados", layout="wide")

st.title("Aplicação de Análise de Dados")
st.divider()

@st.cache_data
def carregar_dataset_exemplo(nome):
    if nome == "Iris":
        dados = load_iris()
        df = pd.DataFrame(dados.data, columns=dados.feature_names)
        df['species'] = pd.Categorical.from_codes(dados.target, dados.target_names)
        return df
    elif nome == "California Housing":
        dados = fetch_california_housing()
        df = pd.DataFrame(dados.data, columns=dados.feature_names)
        df['price'] = dados.target
        return df
    return None

st.sidebar.header("Configurações")

opcao_dados = st.sidebar.radio(
    "Fonte dos dados:",
    ["Upload de arquivo", "Dataset de exemplo"]
)

df = None

if opcao_dados == "Upload de arquivo":
    st.sidebar.subheader("Upload de Arquivo")
    arquivo = st.sidebar.file_uploader(
        "Selecione seu arquivo CSV ou Excel",
        type=['csv', 'xlsx', 'xls']
    )

    if arquivo is not None:
        try:
            if arquivo.name.endswith('.csv'):
                df = pd.read_csv(arquivo)
            else:
                df = pd.read_excel(arquivo)
            st.sidebar.success(f"Arquivo carregado: {arquivo.name}")
        except Exception as e:
            st.sidebar.error(f"Erro ao carregar: {e}")
else:
    dataset_escolhido = st.sidebar.selectbox(
        "Selecione o dataset:",
        ["Iris", "California Housing"]
    )
    df = carregar_dataset_exemplo(dataset_escolhido)
    if df is not None:
        st.sidebar.success(f"Dataset carregado: {dataset_escolhido}")

if df is not None:

    st.header("Visão Geral dos Dados")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Linhas", df.shape[0])
    with col2:
        st.metric("Colunas", df.shape[1])
    with col3:
        st.metric("Valores Nulos", df.isnull().sum().sum())

    st.subheader("Prévia dos Dados")
    num_linhas = st.slider("Número de linhas:", 5, 50, 10)
    st.dataframe(df.head(num_linhas), use_container_width=True)

    st.divider()

    st.header("Estatísticas Descritivas")

    colunas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()

    if len(colunas_numericas) > 0:
        st.subheader("Resumo Estatístico")
        st.dataframe(df.describe(), use_container_width=True)

        st.subheader("Análise por Coluna")
        coluna_selecionada = st.selectbox("Selecione uma coluna:", colunas_numericas)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Média", f"{df[coluna_selecionada].mean():.2f}")
        with col2:
            st.metric("Mediana", f"{df[coluna_selecionada].median():.2f}")
        with col3:
            st.metric("Desvio Padrão", f"{df[coluna_selecionada].std():.2f}")
        with col4:
            st.metric("Variância", f"{df[coluna_selecionada].var():.2f}")

        col5, col6, col7, col8 = st.columns(4)
        with col5:
            st.metric("Mínimo", f"{df[coluna_selecionada].min():.2f}")
        with col6:
            st.metric("Máximo", f"{df[coluna_selecionada].max():.2f}")
        with col7:
            st.metric("Q1 (25%)", f"{df[coluna_selecionada].quantile(0.25):.2f}")
        with col8:
            st.metric("Q3 (75%)", f"{df[coluna_selecionada].quantile(0.75):.2f}")
    else:
        st.warning("Nenhuma coluna numérica encontrada.")

    st.divider()

    st.header("Visualizações")

    if len(colunas_numericas) > 0:

        tab1, tab2, tab3, tab4 = st.tabs(["Histograma", "Gráfico de Dispersão", "Box Plot", "Correlação"])

        with tab1:
            st.subheader("Histograma")
            st.caption("Distribuição de frequência dos valores")

            coluna_hist = st.selectbox("Coluna:", colunas_numericas, key='hist')
            bins = st.slider("Bins:", 5, 50, 20)

            fig = px.histogram(df, x=coluna_hist, nbins=bins,
                             title=f'Distribuição de {coluna_hist}',
                             labels={coluna_hist: coluna_hist, 'count': 'Frequência'})
            fig.update_layout(showlegend=False, height=500)
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            st.subheader("Gráfico de Dispersão")
            st.caption("Relação entre duas variáveis")

            col1, col2 = st.columns(2)
            with col1:
                eixo_x = st.selectbox("Eixo X:", colunas_numericas, key='scatter_x')
            with col2:
                eixo_y = st.selectbox("Eixo Y:", colunas_numericas,
                                     index=min(1, len(colunas_numericas)-1), key='scatter_y')

            colunas_categoricas = df.select_dtypes(include=['object', 'category']).columns.tolist()
            cor_por = None
            if len(colunas_categoricas) > 0:
                usar_cor = st.checkbox("Colorir por categoria")
                if usar_cor:
                    cor_por = st.selectbox("Categoria:", colunas_categoricas)

            fig = px.scatter(df, x=eixo_x, y=eixo_y, color=cor_por,
                           title=f'{eixo_y} vs {eixo_x}',
                           labels={eixo_x: eixo_x, eixo_y: eixo_y})
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)

        with tab3:
            st.subheader("Box Plot")
            st.caption("Distribuição dos dados com quartis e outliers")

            colunas_box = st.multiselect(
                "Selecione as colunas:",
                colunas_numericas,
                default=colunas_numericas[:min(3, len(colunas_numericas))]
            )

            if len(colunas_box) > 0:
                df_melted = df[colunas_box].melt(var_name='Coluna', value_name='Valor')
                fig = px.box(df_melted, x='Coluna', y='Valor',
                           title='Comparação de Distribuições')
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Selecione pelo menos uma coluna.")

        with tab4:
            st.subheader("Matriz de Correlação")
            st.caption("Correlação entre variáveis numéricas")

            if len(colunas_numericas) > 1:
                corr = df[colunas_numericas].corr()

                fig = px.imshow(corr,
                              text_auto='.2f',
                              aspect='auto',
                              color_continuous_scale='RdBu_r',
                              color_continuous_midpoint=0,
                              title='Matriz de Correlação')
                fig.update_layout(height=600)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Necessário pelo menos duas colunas numéricas.")

    st.divider()

    st.header("Filtragem de Dados")

    df_filtrado = df.copy()

    col1, col2 = st.columns(2)

    with col1:
        if len(colunas_numericas) > 0:
            st.subheader("Filtro Numérico")
            coluna_filtro = st.selectbox("Coluna:", colunas_numericas, key='filtro')

            min_val = float(df[coluna_filtro].min())
            max_val = float(df[coluna_filtro].max())

            valores_range = st.slider(
                f"Intervalo de {coluna_filtro}:",
                min_val, max_val, (min_val, max_val)
            )

            df_filtrado = df_filtrado[
                (df_filtrado[coluna_filtro] >= valores_range[0]) &
                (df_filtrado[coluna_filtro] <= valores_range[1])
            ]

    with col2:
        colunas_categoricas = df.select_dtypes(include=['object', 'category']).columns.tolist()
        if len(colunas_categoricas) > 0:
            st.subheader("Filtro Categórico")
            coluna_cat = st.selectbox("Coluna:", colunas_categoricas)
            categorias_unicas = df[coluna_cat].unique().tolist()
            categorias_selecionadas = st.multiselect(
                f"Categorias:",
                categorias_unicas,
                default=categorias_unicas
            )

            if len(categorias_selecionadas) > 0:
                df_filtrado = df_filtrado[df_filtrado[coluna_cat].isin(categorias_selecionadas)]

    st.subheader("Resultado")
    total_original = len(df)
    total_filtrado = len(df_filtrado)
    percentual = (total_filtrado/total_original*100) if total_original > 0 else 0

    st.info(f"Exibindo {total_filtrado} de {total_original} linhas ({percentual:.1f}%)")
    st.dataframe(df_filtrado, use_container_width=True)

    st.download_button(
        label="Baixar dados filtrados (CSV)",
        data=df_filtrado.to_csv(index=False).encode('utf-8'),
        file_name='dados_filtrados.csv',
        mime='text/csv'
    )

else:
    st.info("Selecione uma fonte de dados na barra lateral para começar.")

    st.markdown("""
    ### Instruções

    **Passo 1:** Escolha a fonte de dados
    - Upload de arquivo CSV ou Excel
    - Dataset de exemplo (Iris ou California Housing)

    **Passo 2:** Explore os dados
    - Visualize a tabela de dados
    - Analise estatísticas descritivas
    - Crie gráficos interativos
    - Filtre os dados

    **Passo 3:** Exporte os resultados
    - Baixe os dados filtrados em CSV
    """)
