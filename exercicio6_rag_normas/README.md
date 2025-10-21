# Assistente Virtual RAG - Consulta de Normas Tecnicas

Sistema de consulta de normas tecnicas utilizando RAG (Retrieval Augmented Generation) com AWS Bedrock.

## Arquitetura

O sistema implementa uma arquitetura RAG completa com as seguintes camadas:

### 1. Carregamento de Documentos
- Leitura de normas tecnicas em formato texto (.txt)
- Divisao em fragmentos (chunks) de 500 caracteres com sobreposicao de 50 caracteres
- Preservacao de metadados (fonte, secao, tipo)

### 2. Embeddings
- **Modelo Principal**: Amazon Titan Embeddings via AWS Bedrock
- **Fallback**: Modelo alternativo baseado em hash para desenvolvimento
- Dimensao: 1536 (Titan) ou 384 (alternativo)

### 3. Banco Vetorial
- Utilizacao do ChromaDB para armazenamento vetorial
- Busca por similaridade cosseno
- Persistencia local para reuso

### 4. Geracao de Respostas
- Utilizacao do Amazon Nova Micro via AWS Bedrock
- Prompt engineering para garantir citacao de fontes
- Mecanismo de verificacao de escopo

## Estrutura do Projeto

```
exercicio6_rag_normas/
├── documentos/                  # Normas tecnicas (TXT)
│   ├── norma_001_seguranca_eletrica.txt
│   ├── norma_002_construcao_civil.txt
│   └── norma_003_seguranca_trabalho.txt
├── src/
│   ├── __init__.py
│   ├── configuracao.py          # Configuracoes do sistema
│   ├── carregador_documentos.py # Carregamento e processamento
│   ├── modelo_embeddings.py     # Geracao de embeddings
│   ├── banco_vetorial.py        # Gerenciamento do ChromaDB
│   ├── gerador_respostas.py     # Integracao com LLM
│   └── assistente_rag.py        # Orquestracao do sistema
├── main.py                      # Ponto de entrada principal
├── gerar_exemplos.py            # Script para gerar exemplos
├── requirements.txt
├── .env.example
└── README.md
```

## Instalacao

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar credenciais AWS

Copie o arquivo `.env.example` para `.env` e adicione suas credenciais:

```
AWS_BEARER_TOKEN_BEDROCK=seu_token_aqui
AWS_REGION=us-east-2
AWS_INFERENCE_PROFILE_ID=us.amazon.nova-micro-v1:0
```

### 3. Indexar documentos

```bash
python main.py indexar
```

Este comando:
- Carrega todos os documentos da pasta `documentos/`
- Divide em fragmentos (chunks)
- Gera embeddings para cada fragmento
- Cria e persiste o banco vetorial

## Uso

### Modo Interativo

```bash
python main.py
```

Exemplo de sessao:

```
Pergunta: Qual a secao minima de condutores para iluminacao?

Resposta:
De acordo com a Norma Tecnica 001 - Seguranca em Instalacoes Eletricas,
Secao 3.1, a secao minima de condutores para circuitos de iluminacao é
1,5 mm².

Fonte: norma_001_seguranca_eletrica.txt, Secao 3: Requisitos de Instalacao
```

### Gerar Exemplos

```bash
python gerar_exemplos.py
```

Gera arquivo `exemplos_consultas.txt` com 5 consultas pre-definidas e suas respostas.

## Funcionamento do RAG

### Fluxo de Consulta

1. **Entrada**: Usuario faz uma pergunta em linguagem natural
2. **Embedding da Pergunta**: Converte a pergunta em vetor numerico
3. **Busca por Similaridade**: Encontra os 3 fragmentos mais relevantes no banco vetorial
4. **Construcao do Contexto**: Monta contexto com os fragmentos e metadados
5. **Geracao da Resposta**: LLM gera resposta baseada apenas no contexto
6. **Validacao**: Verifica se a informacao esta no escopo dos documentos
7. **Saida**: Retorna resposta com citacao das fontes

### Prompt Engineering

O sistema utiliza prompt especifico que:
- Instrui a LLM a usar APENAS informacoes do contexto
- Exige citacao de fontes (documento e secao)
- Define resposta padrao para informacoes fora do escopo
- Mantem temperatura baixa (0.1) para respostas deterministicas

### Citacao de Fontes

Cada resposta inclui:
- Nome do documento de origem
- Secao especifica da norma
- Trecho relevante do texto

Exemplo:
```
Fonte: norma_002_construcao_civil.txt
Secao 3.1: Resistencia do Concreto
```

## Normas Incluidas

### Norma 001 - Seguranca em Instalacoes Eletricas
- Secoes minimas de condutores
- Dispositivos de protecao
- Aterramento
- Distancias de seguranca
- Padronizacao de cores

### Norma 002 - Construcao Civil
- Fundacoes
- Estruturas de concreto
- Alvenaria
- Impermeabilizacao
- Instalacoes hidraulicas
- Acessibilidade

### Norma 003 - Seguranca no Trabalho
- Equipamentos de protecao individual
- Andaimes
- Escavacoes
- Instalacoes eletricas temporarias
- Protecao contra quedas

## Limitacoes e Escopo

O assistente:
- ✓ Responde sobre informacoes presentes nas normas indexadas
- ✓ Cita fontes especificas e secoes
- ✓ Mantem precisao sobre valores tecnicos
- ✗ Nao responde sobre normas nao indexadas
- ✗ Nao fornece interpretacoes juridicas
- ✗ Nao substitui consulta a normas oficiais atualizadas

## Tecnologias Utilizadas

- **LangChain**: Framework para aplicacoes LLM
- **ChromaDB**: Banco de dados vetorial
- **AWS Bedrock**: Servico de IA generativa
- **Amazon Titan Embeddings**: Modelo de embeddings
- **Amazon Nova Micro**: Modelo de linguagem
- **Python 3.8+**: Linguagem de programacao

## Possibilidades de Expansao

- Adicionar suporte a documentos PDF
- Implementar cache de respostas frequentes
- Adicionar interface web
- Implementar atualizacao incremental do indice
- Adicionar metricas de confianca nas respostas
- Suportar multiplos idiomas
