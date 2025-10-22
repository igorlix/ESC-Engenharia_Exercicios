# Assistente Virtual RAG - Consulta de Normas Técnicas

Este sistema de consulta de normas técnicas utiliza RAG (Retrieval Augmented Generation) com AWS Bedrock (mesma API dos exercícios anteriores) e demais ferramentas, como:

- **LangChain**: Framework para aplicações LLM
- **ChromaDB**: Banco de dados vetorial
- **Amazon Titan Embeddings**: Modelo de embeddings
- **Amazon Nova Micro**: Modelo de linguagem
- **Python 3.8+**: Linguagem de programação

Infelizmente a comunicação é através do terminal. Tentei criar uma interface para o assistente, mas não terminei a tempo. Ainda assim, é completamente funcional.


## Instalação

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Configuração

Os dados da API estão no arquivo .env

```
AWS_BEARER_TOKEN_BEDROCK=egfsgsegsgegsgeehhser
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

Exemplo de sessão:

```
Pergunta: Qual a seção mínima de condutores para iluminação?

Resposta:
De acordo com a Norma Técnica 001 - Segurança em Instalações Elétricas,
Seção 3.1, a seção mínima de condutores para circuitos de iluminação é
1,5 mm².

Fonte: norma_001_seguranca_eletrica.txt, Seção 3: Requisitos de Instalação
```

### Gerar Exemplos

```bash
python gerar_exemplos.py
```

Gera arquivo `exemplos_consultas.txt` com 5 consultas pré-definidas e suas respostas.


## Arquitetura

O sistema implementa uma arquitetura RAG completa com as seguintes camadas:

### 1. Carregamento de Documentos
- Leitura de normas técnicas em formato texto (.txt)
- Divisão em fragmentos (chunks) de 500 caracteres com sobreposição de 50 caracteres
- Preservação de metadados (fonte, seção, tipo)

### 2. Embeddings
- **Modelo Principal**: Amazon Titan Embeddings via AWS Bedrock
- **Fallback**: Modelo alternativo baseado em hash para desenvolvimento
- **Dimensão**: 1536 (Titan) ou 384 (alternativo)

### 3. Banco Vetorial
- Utilização do ChromaDB para armazenamento vetorial
- Busca por similaridade cosseno
- Persistência local para reuso

### 4. Geração de Respostas
- Utilização do Amazon Nova Micro via AWS Bedrock
- Prompt engineering para garantir citação de fontes
- Mecanismo de verificação de escopo


## Funcionamento do RAG

### Fluxo de Consulta

1. **Entrada**: Usuário faz uma pergunta em linguagem natural
2. **Embedding da Pergunta**: Converte a pergunta em vetor numérico
3. **Busca por Similaridade**: Encontra os 3 fragmentos mais relevantes no banco vetorial
4. **Construção do Contexto**: Monta contexto com os fragmentos e metadados
5. **Geração da Resposta**: LLM gera resposta baseada apenas no contexto
6. **Validação**: Verifica se a informação está no escopo dos documentos
7. **Saída**: Retorna resposta com citação das fontes

### Prompt Engineering

O sistema utiliza prompt específico que:
- Instrui a LLM a usar APENAS informações do contexto
- Exige citação de fontes (documento e seção)
- Define resposta padrão para informações fora do escopo
- Mantém temperatura baixa (0.1) para respostas determinísticas

### Citação de Fontes

Cada resposta inclui:
- Nome do documento de origem
- Seção específica da norma
- Trecho relevante do texto

Exemplo:
```
Fonte: norma_002_construcao_civil.txt
Seção 3.1: Resistência do Concreto
```

## Normas Incluídas

### Norma 001 - Segurança em Instalações Elétricas
- Seções mínimas de condutores
- Dispositivos de proteção
- Aterramento
- Distâncias de segurança
- Padronização de cores

### Norma 002 - Construção Civil
- Fundações
- Estruturas de concreto
- Alvenaria
- Impermeabilização
- Instalações hidráulicas
- Acessibilidade

### Norma 003 - Segurança no Trabalho
- Equipamentos de proteção individual
- Andaimes
- Escavações
- Instalações elétricas temporárias
- Proteção contra quedas

## Limitações

O assistente:
- ✓ Responde sobre informações presentes nas normas indexadas
- ✓ Cita fontes específicas e seções
- ✓ Mantém precisão sobre valores técnicos
- ✗ Não responde sobre normas não indexadas
- ✗ Não fornece interpretações jurídicas
- ✗ Não substitui consulta a normas oficiais atualizadas
