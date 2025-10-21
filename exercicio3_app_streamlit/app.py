import streamlit as st
import pandas as pd
from utils import carregar_dataset_exemplo
from modulos import inicio, visao_geral, estatisticas, graficos, filtros, ajuda

# Configuração da página
st.set_page_config(
    page_title="Análise de Dados",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar - Configurações
with st.sidebar:
    st.header("Configurações")
    st.divider()

    # Seleção da página
    st.subheader("Navegação")
    pagina = st.radio(
        "Selecione a página:",
        ["Início", "Visão Geral", "Estatísticas", "Gráficos", "Filtros", "Ajuda"]
    )

    st.divider()
    st.subheader("Fonte de Dados")

    opcao_dados = st.radio(
        "Escolha a fonte:",
        ["Upload de arquivo", "Dataset de exemplo"]
    )

    df = None

    if opcao_dados == "Upload de arquivo":
        arquivo = st.file_uploader(
            "Carregar arquivo CSV ou Excel",
            type=['csv', 'xlsx', 'xls']
        )

        if arquivo is not None:
            try:
                if arquivo.name.endswith('.csv'):
                    df = pd.read_csv(arquivo)
                else:
                    df = pd.read_excel(arquivo)
                st.success(f"Arquivo carregado: {arquivo.name}")
            except Exception as e:
                st.error(f"Erro ao carregar arquivo: {e}")
    else:
        dataset_escolhido = st.selectbox(
            "Selecione o dataset:",
            ["Iris", "California Housing"]
        )
        df = carregar_dataset_exemplo(dataset_escolhido)
        if df is not None:
            st.success(f"Dataset carregado: {dataset_escolhido}")

    # Armazenar df no session_state
    if df is not None:
        st.session_state['df'] = df

    st.divider()
    st.subheader("Personalização")

    temas = {
        "Padrão": "ggplot2",
        "Seaborn": "seaborn",
        "Plotly": "plotly",
        "Simples": "simple_white"
    }

    tema_selecionado = st.selectbox(
        "Tema dos gráficos:",
        list(temas.keys())
    )

    st.session_state['tema_grafico'] = temas[tema_selecionado]

# Recuperar df do session_state
if 'df' in st.session_state:
    df = st.session_state['df']
else:
    df = None

# Renderizar página selecionada
if pagina == "Início":
    inicio.render(df)
elif pagina == "Visão Geral":
    visao_geral.render(df)
elif pagina == "Estatísticas":
    estatisticas.render(df)
elif pagina == "Gráficos":
    graficos.render(df)
elif pagina == "Filtros":
    filtros.render(df)
elif pagina == "Ajuda":
    ajuda.render(df)
