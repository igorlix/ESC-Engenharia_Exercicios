# Aplicação de Análise de Dados Interativa

Aplicação web para análise exploratória de dados desenvolvida com Streamlit, Pandas e Plotly.

## Funcionalidades

### 6 Páginas Principais

- **Início**: Resumo da aplicação e métricas gerais
- **Visão Geral**: Visualização dos dados, informações de colunas e download
- **Estatísticas**: 12 métricas estatísticas por coluna e histograma de distribuição
- **Gráficos**: 5 tipos de visualizações interativas (Histograma, Dispersão, Box Plot, Correlação, Linha)
- **Filtros**: Filtragem numérica e categórica com exportação
- **Ajuda**: Guia de uso e FAQ

### Recursos

- Upload de CSV/Excel ou datasets de exemplo (Iris e California Housing)
- 4 temas de gráficos (Padrão, Seaborn, Plotly, Simples)
- Gráficos interativos com zoom, pan e download
- Exportação de dados filtrados

## Instalação

```bash
pip install -r requirements.txt
```

## Execução

```bash
streamlit run app.py
```

ou 

```bash
python -m streamlit run app.py
```

A aplicação abrirá automaticamente em http://localhost:8501

## Estrutura do Projeto

```
exercicio3_app_streamlit/
├── app.py              # Aplicação principal
├── utils.py            # Funções auxiliares
├── modulos/            # Módulos das páginas
│   ├── inicio.py
│   ├── visao_geral.py
│   ├── estatisticas.py
│   ├── graficos.py
│   ├── filtros.py
│   └── ajuda.py
└── requirements.txt
```

## Tecnologias

- **Streamlit**: Framework web
- **Pandas**: Manipulação de dados
- **Plotly**: Visualizações interativas
- **Scikit-learn**: Datasets de exemplo
- **NumPy**: Computação numérica

## Uso Básico

1. **Carregar dados**: Use a sidebar para upload de arquivo ou selecione um dataset de exemplo
2. **Navegar**: Escolha uma página no menu lateral
3. **Analisar**: Explore estatísticas, visualizações e aplique filtros
4. **Exportar**: Faça download dos dados completos ou filtrados

## Observações

- Arquivos CSV e Excel suportados
- Sessão mantida enquanto o navegador estiver aberto
- Recomendado para datasets com colunas numéricas e categóricas
