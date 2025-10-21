# Aplicação de Análise de Dados com Streamlit

Aplicação web interativa para análise exploratória de dados, desenvolvida com Streamlit e Pandas.

## Funcionalidades

- Upload de arquivos CSV e Excel
- Datasets de exemplo integrados (Iris e California Housing)
- Visualização de dados em formato de tabela
- Estatísticas descritivas completas (média, mediana, desvio padrão, variância, quartis)
- Múltiplos tipos de gráficos:
  - Histograma
  - Scatter Plot (com opção de colorir por categoria)
  - Box Plot
  - Matriz de Correlação
- Filtragem de dados por valores numéricos e categorias
- Download dos dados filtrados em CSV

## Requisitos

Antes de executar a aplicação, instale as dependências necessárias:

```bash
pip install streamlit pandas numpy matplotlib seaborn scikit-learn openpyxl
```

## Como Executar

### Passo 1: Instalar dependências

```bash
pip install -r requirements.txt
```

Ou instale manualmente:
```bash
pip install streamlit pandas numpy matplotlib seaborn scikit-learn openpyxl
```

### Passo 2: Executar a aplicação

No PowerShell ou terminal, navegue até a pasta do projeto:
```bash
cd exercicio3_app_streamlit
```

E execute:
```bash
python -m streamlit run app.py
```

Ou se o comando `streamlit` estiver no PATH:
```bash
streamlit run app.py
```

### Passo 3: Acessar no navegador

A aplicação será aberta automaticamente no navegador em http://localhost:8501

**Observações:**
- Na primeira execução, o Streamlit pode pedir um email (é opcional, pode deixar em branco)
- NÃO execute com `python app.py` - isso não funciona para aplicações Streamlit!
- Se a porta 8501 estiver ocupada, o Streamlit usará outra porta automaticamente

## Como Usar

### Opção 1: Upload de Arquivo

1. Na barra lateral, selecione "Upload de arquivo"
2. Clique em "Browse files" e selecione um arquivo CSV ou Excel
3. Os dados serão carregados automaticamente

### Opção 2: Dataset de Exemplo

1. Na barra lateral, selecione "Dataset de exemplo"
2. Escolha entre "Iris" ou "California Housing"
3. O dataset será carregado automaticamente

### Explorando os Dados

**Visualização dos Dados**
- Ajuste o número de linhas a serem exibidas usando o slider
- Visualize métricas gerais: total de linhas, colunas e valores nulos

**Estatísticas Descritivas**
- Veja o resumo estatístico completo de todas as colunas numéricas
- Selecione uma coluna específica para ver estatísticas detalhadas

**Visualizações**
- Histograma: Visualize a distribuição de uma variável
- Scatter Plot: Compare duas variáveis numéricas
- Box Plot: Compare distribuições de múltiplas variáveis
- Matriz de Correlação: Veja as correlações entre todas as variáveis numéricas

**Filtragem**
- Filtre dados numéricos usando o slider de intervalo
- Filtre dados categóricos selecionando as categorias desejadas
- Baixe os dados filtrados em formato CSV

## Estrutura do Projeto

```
exercicio3_app_streamlit/
├── app.py          # Código principal da aplicação
└── README.md       # Este arquivo
```

## Datasets Incluídos

**Iris Dataset**
- 150 amostras de flores de 3 espécies diferentes
- 4 features: comprimento e largura das sépalas e pétalas

**California Housing Dataset**
- Dados de preços de imóveis na Califórnia
- 8 features incluindo localização, idade, número de quartos, etc.

## Exemplos de Uso

1. Carregue o dataset Iris
2. Visualize a distribuição da largura das pétalas no histograma
3. Crie um scatter plot comparando comprimento vs largura das pétalas
4. Colorir os pontos por espécie para identificar padrões
5. Filtre apenas as flores da espécie "setosa"
6. Baixe os dados filtrados

## Observações

- Para aproveitar todas as funcionalidades, use datasets com colunas numéricas
- A aplicação detecta automaticamente colunas numéricas e categóricas
- Arquivos muito grandes podem demorar para carregar
- Valores nulos são automaticamente removidos dos gráficos
