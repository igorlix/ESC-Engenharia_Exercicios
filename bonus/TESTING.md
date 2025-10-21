# Guia de Testes - Portal de Exercícios

Este guia detalha como testar o portal localmente antes do deploy na AWS.

## Pré-requisitos

- Docker e Docker Compose instalados
- Credenciais AWS Bedrock (para Ex4 e Ex6)
- Índice RAG criado (para Ex6)

## Preparação

### 1. Configurar Variáveis de Ambiente

```bash
cd bonus
cp api/exercicio4/.env.example api/exercicio4/.env
```

Editar `api/exercicio4/.env`:
```
AWS_BEARER_TOKEN_BEDROCK=seu_token_aqui
AWS_REGION=us-east-2
AWS_INFERENCE_PROFILE_ID=us.amazon.nova-micro-v1:0
```

### 2. Verificar Índice RAG (Exercício 6)

```bash
ls ../exercicio6_rag_normas/banco_vetorial/
```

Se não existir, criar:
```bash
cd ../exercicio6_rag_normas
python main.py --indexar
cd ../bonus
```

## Teste com Docker

### 1. Iniciar Todos os Serviços

```bash
cd docker
docker-compose up --build
```

Aguardar até ver mensagens:
```
apis_1      | Iniciando todas as APIs...
apis_1      | APIs iniciadas:
django_1    | Starting development server at http://0.0.0.0:8000/
streamlit_1 | You can now view your Streamlit app in your browser.
nginx_1     | [notice] ... start worker processes
```

### 2. Verificar Health Checks

Em outro terminal:

```bash
# APIs
curl http://localhost:5001/health
curl http://localhost:5002/health
curl http://localhost:5004/health
curl http://localhost:5006/health

# Django
curl http://localhost:8000/

# Streamlit
curl http://localhost:8501/

# Nginx
curl http://localhost/
```

Todos devem retornar status 200 OK.

### 3. Testar Cada Exercício

#### Exercício 1 - Extração de Emails

```bash
curl -X POST http://localhost:5001/api/ex1/extrair-emails \
  -H "Content-Type: application/json" \
  -d '{"texto":"Contato: joao@exemplo.com e maria@teste.com"}'
```

Esperado:
```json
{
  "emails": ["joao@exemplo.com", "maria@teste.com"],
  "total": 2
}
```

#### Exercício 2 - Classificador de Spam

```bash
curl -X POST http://localhost:5002/api/ex2/classificar \
  -H "Content-Type: application/json" \
  -d '{"mensagem":"Win free iPhone now! Click here!"}'
```

Esperado:
```json
{
  "classificacao": "spam",
  "confianca": 0.85
}
```

#### Exercício 4 - Extração com LLM

```bash
curl -X POST http://localhost:5004/api/ex4/extrair \
  -H "Content-Type: application/json" \
  -d '{"documento":"Relatório Técnico - Projeto X. Autor: João Silva. Data: 2024-01-15"}'
```

Esperado (varia):
```json
{
  "titulo": "Relatório Técnico - Projeto X",
  "autor": "João Silva",
  "data": "2024-01-15"
}
```

#### Exercício 6 - Assistente RAG

```bash
curl -X POST http://localhost:5006/api/ex6/consultar \
  -H "Content-Type: application/json" \
  -d '{"pergunta":"Qual a altura mínima para instalação de tomadas elétricas?"}'
```

Esperado:
```json
{
  "resposta": "De acordo com a norma NBR 5410, a altura mínima é de 30 cm..."
}
```

### 4. Testar Interface Web

Abrir navegador:
- **Portal**: http://localhost/
- **Ex3 (Streamlit)**: http://localhost/ex3/
- **Ex5 (Django)**: http://localhost/ex5/

Verificar:
- ✅ Portal carrega com 6 cards
- ✅ Clicar em Ex1 abre interface de extração de emails
- ✅ Clicar em Ex2 abre interface de classificador
- ✅ Clicar em Ex3 redireciona para Streamlit
- ✅ Clicar em Ex4 abre interface de extração LLM
- ✅ Clicar em Ex5 redireciona para Django
- ✅ Clicar em Ex6 abre interface RAG

### 5. Testar Funcionalidades

#### Ex1 - Extração de Emails
1. Inserir texto: "Contato: teste@exemplo.com"
2. Clicar "Extrair Emails"
3. Verificar resultado: 1 email encontrado

#### Ex2 - Classificador de Spam
1. Inserir mensagem: "Free money now!!!"
2. Clicar "Classificar"
3. Verificar resultado: spam com alta confiança

#### Ex4 - Extração com LLM
1. Inserir documento de teste
2. Clicar "Extrair Informações"
3. Verificar resultado: dados estruturados

#### Ex6 - Assistente RAG
1. Inserir pergunta sobre normas
2. Clicar "Consultar Normas"
3. Verificar resposta com citações

## Testes de Integração

### Teste de CORS

Verificar que frontend consegue comunicar com APIs:

```javascript
// No console do navegador (http://localhost/)
fetch('http://localhost:5001/api/ex1/extrair-emails', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({texto: 'teste@email.com'})
})
.then(r => r.json())
.then(console.log);
```

Não deve dar erro de CORS.

### Teste de Performance

```bash
# Testar carga na API
for i in {1..10}; do
  curl -X POST http://localhost:5001/api/ex1/extrair-emails \
    -H "Content-Type: application/json" \
    -d '{"texto":"teste@email.com"}' &
done
wait
```

Todas as requisições devem completar com sucesso.

## Logs e Debugging

### Ver Logs de Todos os Serviços

```bash
docker-compose logs -f
```

### Ver Logs de Um Serviço Específico

```bash
docker-compose logs -f apis
docker-compose logs -f django
docker-compose logs -f streamlit
docker-compose logs -f nginx
```

### Entrar em um Container

```bash
docker-compose exec apis /bin/bash
docker-compose exec django /bin/bash
docker-compose exec streamlit /bin/bash
```

### Reiniciar um Serviço

```bash
docker-compose restart apis
docker-compose restart django
docker-compose restart streamlit
```

## Problemas Comuns

### Erro: "Cannot connect to Docker daemon"

```bash
# Iniciar Docker
sudo systemctl start docker  # Linux
# ou abrir Docker Desktop (Mac/Windows)
```

### Erro: "port is already allocated"

```bash
# Parar containers conflitantes
docker-compose down
docker ps -a  # Ver todos os containers
docker stop <container_id>
```

### Erro: "exercicio6_rag_normas not found"

O Dockerfile procura a pasta no diretório pai. Verificar estrutura:
```
ESC-Engenharia_Exerc-cios/
├── bonus/
│   └── docker/
└── exercicio6_rag_normas/
```

### Ex6 retorna "Assistente não inicializado"

```bash
# Ver logs
docker-compose logs apis | grep -i ex6

# Verificar se índice existe
docker-compose exec apis ls /app/exercicio6_rag_normas/banco_vetorial/
```

## Limpeza

### Parar Serviços

```bash
docker-compose down
```

### Remover Volumes e Imagens

```bash
docker-compose down -v
docker-compose down --rmi all
```

### Limpar Tudo (Cuidado!)

```bash
docker system prune -a --volumes
```

## Checklist de Testes

Antes de fazer deploy, verificar:

- [ ] Todas as APIs respondem no health check
- [ ] Ex1 extrai emails corretamente
- [ ] Ex2 classifica spam corretamente
- [ ] Ex3 (Streamlit) carrega sem erros
- [ ] Ex4 extrai dados com LLM (requer credenciais AWS)
- [ ] Ex5 (Django) carrega e permite análise de sentimento
- [ ] Ex6 consulta RAG e retorna respostas
- [ ] Frontend carrega em http://localhost/
- [ ] Todos os links funcionam
- [ ] Não há erros de CORS no console do navegador
- [ ] Logs não mostram erros críticos

## Próximos Passos

Após validar localmente:
1. Consultar [README-DEPLOY-AWS.md](README-DEPLOY-AWS.md) para deploy
2. Atualizar URLs em `frontend/js/config.js` para produção
3. Configurar CORS restrito nas APIs
4. Fazer push do código para repositório Git
5. Seguir guia de deploy AWS
