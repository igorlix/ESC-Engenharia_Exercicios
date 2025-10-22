# Exercício 3 - Aplicação de Análise de Dados 

![App:](exercicio3_app_streamlit\modulos\app.png)

Optei por não usar um arquivo único, pois ele estava muito extenso. "app.py" serve como main, os demais métodos estão na pasta "modulos".

Não conhecia o streamlit e tirei muita coisa da ([documentação](https://docs.streamlit.io/)) e [galeria](https://streamlit.io/gallery), especialmente a parte de mostrar código fonte para os gráficos.

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

A aplicação abrirá em http://localhost:8501

## Funcionalidades

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


## Observações

- Arquivos CSV e Excel como entrada
- A sessão mantida enquanto o navegador estiver aberto ou o terminal não for fechado.
- Recomendo datasets com colunas numéricas e categóricas
