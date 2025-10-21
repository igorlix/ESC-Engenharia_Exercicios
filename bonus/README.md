# Portal de Exercícios - ESC Engenharia

Portal web centralizado para demonstração dos 6 exercícios técnicos do processo seletivo de estágio.

## Estrutura do Projeto

```
bonus/
├── frontend/                  # Portal estático (HTML/CSS/JS)
│   ├── index.html            # Menu principal
│   ├── css/style.css         # Estilos (tema dark)
│   ├── js/config.js          # Configuração URLs (local/produção)
│   └── exercicios/           # Páginas individuais
│       ├── ex1.html          # Extração de emails
│       ├── ex2.html          # Classificador spam
│       ├── ex4.html          # Extração Bedrock
│       └── ex6.html          # RAG consulta
│
├── api/                      # APIs REST (Flask)
│   ├── exercicio1/           # API extração emails
│   ├── exercicio2/           # API classificador
│   ├── exercicio4/           # API Bedrock
│   ├── exercicio6/           # API RAG
│   └── requirements.txt
│
├── docker/                   # Arquivos Docker
│   ├── Dockerfile.apis       # Container para APIs Flask
│   ├── Dockerfile.django     # Container para Django (Ex5)
│   ├── Dockerfile.streamlit  # Container para Streamlit (Ex3)
│   ├── docker-compose.yml    # Orquestração de serviços
│   ├── nginx.conf            # Configuração Nginx
│   └── start-apis.sh         # Script inicialização APIs
│
├── README.md                 # Este arquivo
├── README-DEPLOY-AWS.md      # Guia completo de deploy AWS
└── TESTING.md                # Guia de testes e troubleshooting
```

## Exercícios Disponíveis

### Com Interface Web (redirecionamento)
- **Exercício 3**: Streamlit - Análise de dados
- **Exercício 5**: Django - Análise de sentimento

### Com API REST
- **Exercício 1**: Extração de emails
- **Exercício 2**: Classificador de spam
- **Exercício 4**: Extração com AWS Bedrock
- **Exercício 6**: Assistente RAG para normas técnicas

## Instalação e Uso

### Pré-requisitos

- Docker instalado
- Docker Compose instalado
- Credenciais AWS Bedrock (para Ex4 e Ex6)

### 1. Configurar Variáveis de Ambiente

```bash
cd bonus
cp api/exercicio4/.env.example api/exercicio4/.env
```

Edite `api/exercicio4/.env` com suas credenciais AWS:
```
AWS_BEARER_TOKEN_BEDROCK=seu_token_aqui
AWS_REGION=us-east-2
AWS_INFERENCE_PROFILE_ID=us.amazon.nova-micro-v1:0
```

### 2. Iniciar Todos os Serviços

```bash
cd docker
docker-compose up --build
```

Aguarde até ver as mensagens:
```
apis_1      | APIs iniciadas:
django_1    | Starting development server at http://0.0.0.0:8000/
streamlit_1 | You can now view your Streamlit app in your browser.
nginx_1     | start worker processes
```

Isso iniciará todos os serviços:
- APIs Flask (portas 5001, 5002, 5004, 5006)
- Django (porta 8000)
- Streamlit (porta 8501)
- Nginx (porta 80 - ponto de entrada principal)

### 3. Acessar o Portal

Abra o navegador em: **http://localhost/**

URLs diretas:
- **Portal Principal**: http://localhost/
- **APIs**: http://localhost/api/ex1/, http://localhost/api/ex2/, etc.
- **Django (Ex5)**: http://localhost/ex5/
- **Streamlit (Ex3)**: http://localhost/ex3/

### 4. Parar os Serviços

```bash
docker-compose down
```

Para limpar tudo (volumes e imagens):
```bash
docker-compose down -v --rmi all
```

## Arquitetura

### Frontend
- HTML5 + CSS3 + JavaScript puro
- Tema dark inspirado no exercício 5
- Comunicação via Fetch API
- CORS habilitado

### Backend
- 4 APIs Flask independentes
- Cada API roda em porta separada
- Reutiliza código dos exercícios originais
- CORS configurado para desenvolvimento local

### Comunicação
```
Browser (frontend/index.html)
    ↓
APIs Flask (localhost:500x)
    ↓
Código dos Exercícios Originais
```

## Deploy na AWS

Para instruções completas de deploy na AWS, consulte o arquivo [README-DEPLOY-AWS.md](README-DEPLOY-AWS.md).

### Resumo das Opções

#### Opção 1: Docker + EC2 (Recomendado para começar)
- 1x EC2 t3.medium (~$30/mês)
- S3 + CloudFront (~$5/mês)
- **Total: ~$35/mês**
- Mais simples, controle total

#### Opção 2: ECS Fargate
- Containers gerenciados
- Auto-scaling automático
- **Total: ~$50-70/mês**

#### Opção 3: Serverless (Lambda)
- Mais econômico para baixo tráfego
- **Total: ~$10-20/mês**
- Requer adaptação do código

### Arquitetura AWS (Opção 1)

```
Internet → CloudFront → S3 (frontend estático)
                     ↓
                  ALB (opcional)
                     ↓
              EC2 (Docker Containers)
              - APIs (Ex 1,2,4,6)
              - Django (Ex 5)
              - Streamlit (Ex 3)
```

## Estrutura de Portas

| Exercício | Tipo | Porta | URL |
|-----------|------|-------|-----|
| 1 | API | 5001 | http://localhost:5001 |
| 2 | API | 5002 | http://localhost:5002 |
| 3 | Web | 8501 | http://localhost:8501 |
| 4 | API | 5004 | http://localhost:5004 |
| 5 | Web | 8000 | http://localhost:8000 |
| 6 | API | 5006 | http://localhost:5006 |

## Endpoints da API

### Exercício 1
```
POST /api/ex1/extrair-emails
Body: {"texto": "email@example.com"}
Response: {"emails": ["email@example.com"], "total": 1}
```

### Exercício 2
```
POST /api/ex2/classificar
Body: {"mensagem": "Win free iPhone!"}
Response: {"classificacao": "spam", "confianca": 0.95}
```

### Exercício 4
```
POST /api/ex4/extrair
Body: {"documento": "texto do documento..."}
Response: {"titulo": "...", "autor": "...", ...}
```

### Exercício 6
```
POST /api/ex6/consultar
Body: {"pergunta": "Qual a altura mínima de tomadas?"}
Response: {"resposta": "30 cm conforme norma..."}
```

## Desenvolvimento

### Adicionar Novo Exercício

1. Criar pasta `api/exercicio<N>/`
2. Criar `app.py` com Flask
3. Adicionar rota em `/api/ex<N>/<endpoint>`
4. Criar página HTML em `frontend/exercicios/ex<N>.html`
5. Adicionar card em `frontend/index.html`
6. Atualizar `js/config.js` com nova URL

### Testar APIs

```bash
# Health check
curl http://localhost:5001/health

# Testar endpoint
curl -X POST http://localhost:5001/api/ex1/extrair-emails \
  -H "Content-Type: application/json" \
  -d '{"texto":"contato@empresa.com"}'
```

### Configuração de URLs

O arquivo `frontend/js/config.js` detecta automaticamente o ambiente:

```javascript
const ENV = window.location.hostname === 'localhost' ? 'local' : 'production';
const API_URLS = CONFIG[ENV];
```

Para alterar URLs de produção, editar `config.js` na seção `production`.

## Troubleshooting

### Docker

**Container não inicia:**
```bash
# Ver logs
docker-compose logs -f

# Reconstruir imagens
docker-compose build --no-cache

# Limpar volumes
docker-compose down -v
```

**API não responde:**
```bash
# Verificar status
docker-compose ps

# Ver logs específicos
docker-compose logs apis
docker-compose logs django
docker-compose logs streamlit
```

**Erro de porta em uso:**
```bash
# Parar todos os containers
docker-compose down

# Verificar portas em uso (Linux/Mac)
lsof -i :80
lsof -i :5001

# Matar processo (exemplo)
kill -9 <PID>
```

### APIs

**Erro de CORS:**
- Verificar CORS configurado em cada `app.py`
- Verificar URL correta no `config.js`
- Testar em modo anônimo do navegador

**Exercício 6 não responde:**
```bash
# Verificar se índice existe
ls ../exercicio6_rag_normas/banco_vetorial/

# Criar índice se necessário
cd ../exercicio6_rag_normas
python main.py --indexar
```

**Exercício 4 erro AWS:**
- Verificar credenciais no arquivo `.env`
- Testar token: `aws bedrock list-foundation-models --region us-east-2`

## Observações

- As APIs reutilizam o código original dos exercícios
- Nenhum arquivo dos exercícios originais foi modificado
- O frontend é 100% estático (pode ser hospedado em qualquer lugar)
- CORS está habilitado para desenvolvimento local
- Para produção, restringir CORS para domínios específicos
- Docker Compose orquestra todos os serviços em um único comando

## Licença

Desenvolvido para processo seletivo de estágio - ESC Engenharia
