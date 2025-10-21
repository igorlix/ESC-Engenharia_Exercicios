import streamlit as st

def render(df=None):
    """Renderiza a página Ajuda"""
    st.markdown("# <span style='color: #ff4b4b;'>Central de Ajuda</span>", unsafe_allow_html=True)

    st.markdown("""
    Esta aplicação foi desenvolvida para facilitar a análise exploratória de dados.
    Abaixo você encontrará um guia completo de uso.
    """)

    st.divider()

    # Seção: Primeiros Passos
    st.markdown("## <span style='color: #ff8c42;'>Primeiros Passos</span>", unsafe_allow_html=True)

    with st.expander("Como carregar dados?", expanded=True):
        st.markdown("""
        **Upload de Arquivo**
        1. Use a barra lateral à esquerda
        2. Selecione "Upload de arquivo"
        3. Clique no botão e escolha seu arquivo (.csv, .xlsx, .xls)
        4. Aguarde o carregamento

        **Dataset de Exemplo**
        1. Use a barra lateral à esquerda
        2. Selecione "Dataset de exemplo"
        3. Escolha entre Iris ou California Housing
        """)

    with st.expander("Como navegar pelas páginas?"):
        st.markdown("""
        Use o menu de navegação na barra lateral:

        - **Início**: Página inicial com resumo geral
        - **Visão Geral**: Visualize os dados completos e informações das colunas
        - **Estatísticas**: Análise estatística detalhada
        - **Gráficos**: Visualizações interativas variadas
        - **Filtros**: Filtre e exporte subconjuntos dos dados
        - **Ajuda**: Esta página de ajuda
        """)

    st.divider()

    # Seção: Funcionalidades por Página
    st.markdown("## <span style='color: #ff8c42;'>Funcionalidades por Página</span>", unsafe_allow_html=True)

    with st.expander("Visão Geral"):
        st.markdown("""
        **O que você encontra nesta página:**

        - Métricas principais: número de linhas, colunas, tamanho em memória, valores nulos
        - Prévia dos dados: visualize as primeiras linhas do dataset
        - Informações das colunas: tipo de dados, valores nulos por coluna
        - Download: exporte os dados completos em CSV ou Excel

        **Dica:** Use o slider para ajustar quantas linhas deseja visualizar na prévia.
        """)

    with st.expander("Estatísticas"):
        st.markdown("""
        **O que você encontra nesta página:**

        - Resumo estatístico completo: média, desvio padrão, quartis, etc.
        - Análise detalhada por coluna com 12 métricas:
          - Média, mediana, moda
          - Desvio padrão, variância
          - Mínimo, máximo, quartis
          - IQR, assimetria e curtose
        - Visualização da distribuição: histograma da coluna selecionada

        **Nota:** A assimetria indica se os dados estão concentrados à esquerda ou direita da média.
        A curtose indica o quão "pontiaguda" é a distribuição.
        """)

    with st.expander("Gráficos"):
        st.markdown("""
        **Tipos de gráficos disponíveis:**

        **Histograma**
        - Visualize a distribuição de frequência de uma variável
        - Ajuste o número de bins para mais ou menos detalhes

        **Dispersão (Scatter Plot)**
        - Compare duas variáveis numéricas
        - Adicione cores por categoria para análise mais profunda

        **Box Plot**
        - Compare distribuições de múltiplas variáveis
        - Identifique outliers visualmente

        **Correlação**
        - Veja a matriz de correlação entre todas as variáveis
        - Identifique as correlações mais fortes

        **Linha**
        - Visualize tendências ao longo dos índices
        - Compare múltiplas variáveis simultaneamente

        **Dica:** Altere o tema dos gráficos na barra lateral em "Personalização".
        """)

    with st.expander("Filtros"):
        st.markdown("""
        **Como usar os filtros:**

        **Filtro Numérico**
        1. Selecione uma coluna numérica
        2. Use o slider para definir o intervalo desejado
        3. Os dados serão filtrados automaticamente

        **Filtro Categórico**
        1. Selecione uma coluna categórica
        2. Escolha quais categorias deseja manter
        3. Os dados serão filtrados automaticamente

        **Exportar dados filtrados:**
        - Use os botões de download para exportar apenas os dados que passaram pelos filtros
        - Formato CSV ou Excel disponível

        **Dica:** Você pode combinar filtros numéricos e categóricos simultaneamente.
        """)

    st.divider()

    # Seção: FAQ
    st.markdown("## <span style='color: #ff8c42;'>Perguntas Frequentes (FAQ)</span>", unsafe_allow_html=True)

    with st.expander("Qual o tamanho máximo de arquivo suportado?"):
        st.markdown("""
        O limite depende da memória disponível no servidor. Recomendamos:
        - CSV: Até 200 MB
        - Excel: Até 50 MB

        Para arquivos maiores, considere filtrar ou amostrar os dados antes do upload.
        """)

    with st.expander("Os dados ficam salvos no servidor?"):
        st.markdown("""
        Não. Todos os dados são processados apenas durante sua sessão.
        Quando você fecha a aplicação ou recarrega a página, os dados são removidos.
        Seus dados estão seguros e privados.
        """)

    with st.expander("Como interpretar a matriz de correlação?"):
        st.markdown("""
        - Valores próximos a +1: Correlação positiva forte (quando uma sobe, a outra também sobe)
        - Valores próximos a -1: Correlação negativa forte (quando uma sobe, a outra desce)
        - Valores próximos a 0: Pouca ou nenhuma correlação linear

        Cores: Azul = correlação negativa, Vermelho = correlação positiva
        """)

    st.divider()

    # Rodapé
    st.info("""
    Esta aplicação foi desenvolvida como parte do Exercício 3 - ESC Engenharia.
    Desenvolvido com Streamlit, Pandas e Plotly.
    """)
