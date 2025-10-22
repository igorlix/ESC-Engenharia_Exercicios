# Análise de Sentimento Web

Para aplicação web, como especificado, utilizei:

- Django
- AWS Bedrock (Amazon Nova Micro) - LLM para análise
- TextBlob + Dicionário de palavras - Fallback local (Caso o token falhe, o sistema automaticamente usa esses métodos)
- Bootstrap 5 - Interface 
- SQLite - Banco de dados

Com relação a chave de api do LLM, estou usando a mesma do exercício 4.


## Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Baixe os dados do TextBlob (necessário apenas na primeira vez):
```bash
python -m textblob.download_corpora
```

3. Execute as migrações do banco de dados:
```bash
python manage.py migrate
```

4. Crie um usuário administrador (opcional):
```bash
python manage.py createsuperuser
```

## Execução

Inicie o servidor de desenvolvimento:
```bash
python manage.py runserver
```

Acesse a aplicação em: http://localhost:8000

## Funcionalidades

- Sistema de login e registro de usuários
- Análise de sentimento de textos (positivo, negativo, neutro)
- Pontuação numérica da análise (-1.0 a 1.0)
- Histórico de análises por usuário
- Menu de exemplos para testes rápidos
- Suporte a análise com LLM (AWS Bedrock) ou fallback local


## Análise de Sentimento

### Métodos de Análise

#### 1. AWS Bedrock + LLM (Preferencial)
Se as credenciais AWS estiverem configuradas no arquivo `.env`, o sistema usa o modelo Amazon Nova Micro via AWS Bedrock para análise de sentimento.

#### 2. Dicionário de Palavras (Fallback Principal)
Caso a LLM não esteja disponível ou falhe, o sistema utiliza um dicionário com palavras em português e inglês:
- **Palavras positivas**: excelente, ótimo, bom, maravilhoso, perfeito, etc.
- **Palavras negativas**: ruim, péssimo, horrível, terrível, decepcionante, etc.
- Cálculo baseado na proporção de palavras positivas vs negativas

#### 3. TextBlob (Fallback Secundário)
Para textos sem palavras conhecidas no dicionário, o sistema usa TextBlob como última opção. Ele funciona melhor com frases em inglês.

Por essa razão, optei por implementar uma solução híbrida usando.

### Resultado da Análise

Independente do método utilizado, o resultado sempre retorna:
- **Sentimento**: positivo, negativo ou neutro
- **Pontuação**: valor entre -1.0 (muito negativo) e 1.0 (muito positivo)
