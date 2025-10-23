# Assistente Virtual RAG - Consulta de Regulamentos INMETRO

Este sistema de consulta de regulamentos técnicos utiliza RAG (Retrieval Augmented Generation) com AWS Bedrock e outras ferramentas, tais como:

- **LangChain**: Framework para aplicações LLM
- **ChromaDB**: Banco de dados vetorial para busca cosseno
- **Cohere Embed v4**: Modelo de embeddings (1536 dimensões)
- **Amazon Nova Micro**: Modelo de linguagem para geração de respostas
- **PyPDF**: Extração de texto de documentos PDF
- **Python 3.8+**: Linguagem de programação

A comunicação é através do terminal. Como citei no README principal, tentei criar uma interface para o assistente, mas não terminei a tempo. Mesmo assim, é completamente funcional.

## Instalação

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Configuracao

Os dados da API estão no link:

https://drive.google.com/file/d/1RB3BgLQ8CoeEO7RMkyLKPbjcmzotwz67/view?usp=drive_link

Copie e cole no arquivo .env desse exercício

```
AWS_BEARER_TOKEN_BEDROCK=
AWS_REGION=us-east-2
AWS_INFERENCE_PROFILE_ID=us.amazon.nova-micro-v1:0
```


### 3. Indexar documentos

Execute no cmd ou powershell

É normal demorar

```bash
python main.py indexar
```

Este comando:
- Carrega todos os documentos PDF/TXT da pasta `documentos/`
- Extrai texto de cada página dos PDFs
- Divide em fragmentos (chunks) de 1000 caracteres
- Gera embeddings vetoriais para cada fragmento
- Cria e persiste o banco vetorial ChromaDB


## Uso

### Modo Interativo

Execute no cmd ou powershell

```bash
python main.py
```

Exemplo de sessão:

```
Pergunta: Qual a definição de brinquedo segundo o Inmetro?

Resposta:
Segundo a Portaria nº 302/2021 (RTQ para Brinquedos), brinquedo é definido
como qualquer produto ou material destinado ou claramente concebido para ser
utilizado em jogos por crianças com idade inferior a 14 anos.

Fonte: RTAC002801.pdf - Página 5, Seção 3: Definições
```

### Gerar Exemplos

```bash
python gerar_exemplos.py
```

Gera arquivo `exemplos_consultas.txt` com 8 consultas pré-definidas e suas respostas sobre:
- Definição de brinquedos
- Requisitos de segurança para brinquedos com baterias
- Correntes máximas de plugues
- Requisitos para adaptadores (Ele não encontra a resposta, mas achei interessante manter)
- Rotulagem de brinquedos
- Limites químicos
- Padrão brasileiro de tomadas
- Testes mecânicos obrigatórios


## Documentos 

### 1. RTQ para Brinquedos (Portaria nº 302/2021)
**Arquivo**: `RTAC002801.pdf`

Regulamento Técnico da Qualidade para Brinquedos consolidado pelo INMETRO. Define:
- Definição técnica de brinquedo
- Requisitos de segurança mecânicos, químicos e elétricos
- Métodos de ensaio obrigatórios
- Normas de rotulagem e informações ao consumidor
- Limites de substâncias químicas permitidas
- Requisitos para brinquedos com baterias e componentes elétricos

**Fonte**: [INMETRO - RTAC002801](http://www.inmetro.gov.br/legislacao/rtac/pdf/RTAC002801.pdf)

### 2. Regulamento para Plugues e Tomadas (Portaria nº 90/2022)
**Arquivo**: `RTAC002934.pdf`

Regulamento consolidado para avaliação da conformidade de plugues e tomadas de uso doméstico. Inclui:
- Padrão brasileiro de plugues e tomadas (NBR 14136)
- Correntes máximas permitidas
- Requisitos de segurança elétrica
- Especificações para adaptadores
- Ensaios de conformidade
- Marcação e rotulagem obrigatória

**Fonte**: [INMETRO - Portaria 90/2022](http://sistema-sil.inmetro.gov.br/rtac/RTAC002934.pdf)

## Exemplos de Consultas Suportadas

### Sobre Brinquedos (RTQ Portaria 302/2021)
- ✓ "Qual a definição oficial de brinquedo?"
- ✓ "Quais substâncias químicas são proibidas em brinquedos?"
- ✓ "Quais são os requisitos elétricos para brinquedos com bateria?"
- ✓ "Como deve ser a rotulagem de brinquedos importados?"
- ✓ "Quais testes mecânicos são obrigatórios?"
- ✓ "Qual a idade mínima indicativa para brinquedos pequenos?"

### Sobre Plugues e Tomadas (Portaria 90/2022)
- ✓ "Qual o padrão brasileiro de tomadas?"
- ✓ "Qual a corrente máxima suportada por plugues de 10A?"
- ✓ "Adaptadores de tomada precisam de certificação?"
- ✓ "Quais são os requisitos de segurança para plugues?"
- ✓ "Como deve ser a marcação de plugues certificados?"
- ✓ "Quais ensaios são obrigatórios para tomadas?"

## Arquitetura RAG

O sistema implementa uma arquitetura completa de Retrieval Augmented Generation:

### 1. Carregamento de Documentos
- Leitura de PDFs regulatórios do INMETRO
- Extração de texto página por página usando PyPDF
- Suporte adicional para arquivos .txt
- Preservação de metadados (fonte, tipo, número de páginas)

### 2. Processamento e Chunking
- **Divisão inteligente**: chunks de 1000 caracteres (otimizado para PDFs técnicos)
- **Sobreposição**: 100 caracteres entre chunks (preserva contexto)
- **Separadores hierárquicos**: "\n\n" → "\n" → ". " → " " → ""
- **Metadados preservados**: cada chunk mantém referência ao documento original

### 3. Embeddings Vetoriais
- **Modelo Principal**: Cohere Embed v4 via AWS Bedrock (1536 dimensões)
- **Fallback**: TF-IDF para desenvolvimento local (384 dimensões)
- Conversão de texto para representação vetorial densa

### 4. Banco Vetorial (ChromaDB)
- Armazenamento persistente de embeddings
- Busca por similaridade cosseno
- Recuperação dos top-5 fragmentos mais relevantes
- Índice otimizado para consultas rápidas

### 5. Geração de Respostas (LLM)
- **Modelo**: Amazon Nova Micro via AWS Bedrock
- **Temperatura**: 0.3 (respostas determinísticas e precisas)
- **Max Tokens**: 1000
- **Prompt Engineering**: instruções específicas para citação de fontes

## Limitações 

O assistente:

**Capacidades** 
- Responde sobre informações presentes nos regulamentos indexados
- Cita fontes específicas (documento, página, seção)
- Mantém alta precisão sobre valores técnicos e normativos
- Suporta perguntas em linguagem natural
- Funciona offline após indexação inicial

**Limitações** 
- Não responde sobre regulamentos não indexados
- Não fornece interpretações jurídicas ou aconselhamento legal
- Não substitui consulta a documentos oficiais atualizados
- Não acessa informações externas ou da internet
- Limitado aos documentos de brinquedos e plugues/tomadas
