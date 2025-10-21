# Analise de Sentimento Web

Aplicacao web Django para analise de sentimento de textos com sistema de autenticacao.

## Funcionalidades

- Sistema de login e registro de usuarios
- Analise de sentimento de textos (positivo, negativo, neutro)
- Pontuacao numerica da analise (-1.0 a 1.0)
- Historico de analises por usuario
- Menu de exemplos para testes rapidos
- Interface moderna com tema escuro
- Suporte a analise com LLM (AWS Bedrock) ou fallback local

## Requisitos

- Python 3.8 ou superior
- (Opcional) Conta AWS com acesso ao Bedrock para analise com LLM

## Instalacao

1. Instale as dependencias:
```bash
pip install -r requirements.txt
```

2. Baixe os dados do TextBlob (necessario apenas na primeira vez):
```bash
python -m textblob.download_corpora
```

3. (Opcional) Configure credenciais AWS para usar LLM:
```bash
cp .env.example .env
```
Edite o arquivo `.env` com suas credenciais AWS Bedrock.

4. Execute as migracoes do banco de dados:
```bash
python manage.py migrate
```

5. Crie um superusuario (opcional):
```bash
python manage.py createsuperuser
```

## Execucao

Inicie o servidor de desenvolvimento:
```bash
python manage.py runserver
```

Acesse a aplicacao em: http://localhost:8000

## Uso

1. Registre um novo usuario ou faca login
2. Digite um texto na caixa de analise
3. Clique em "Analisar" para obter o resultado
4. Visualize o sentimento detectado e a pontuacao
5. Consulte o historico de analises no painel lateral

## Estrutura do Projeto

```
exercicio5_web_django/
├── projeto/                 # Configuracoes do Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── analise/                 # App principal
│   ├── models.py            # Modelo de dados
│   ├── views.py             # Logica de views
│   ├── urls.py              # Rotas
│   ├── analisador.py        # Analise de sentimento
│   └── templates/           # Templates HTML
├── manage.py
└── requirements.txt
```

## Tecnologias

- Django 4.2
- AWS Bedrock (Amazon Nova Micro) - LLM para analise
- TextBlob + Dicionario de palavras - Fallback local
- Bootstrap 5 - Interface responsiva
- SQLite - Banco de dados

## Analise de Sentimento

### Metodos de Analise

O sistema possui 3 niveis de analise de sentimento com fallback automatico:

#### 1. AWS Bedrock + LLM (Preferencial)
Se as credenciais AWS estiverem configuradas no arquivo `.env`, o sistema usa o modelo Amazon Nova Micro via AWS Bedrock para analise de sentimento. Este metodo oferece:
- Maior precisao na analise de contexto
- Melhor compreensao de textos complexos
- Suporte nativo a portugues e ingles

#### 2. Dicionario de Palavras (Fallback Principal)
Caso a LLM nao esteja disponivel ou falhe, o sistema utiliza um dicionario customizado com mais de 60 palavras em portugues e ingles:
- **Palavras positivas**: excelente, otimo, bom, maravilhoso, perfeito, etc.
- **Palavras negativas**: ruim, pessimo, horrivel, terrivel, decepcionante, etc.
- Calculo baseado na proporcao de palavras positivas vs negativas

#### 3. TextBlob (Fallback Secundario)
Para textos sem palavras conhecidas no dicionario, o sistema usa TextBlob como ultima opcao:
- Funciona melhor com textos em ingles
- Resultados limitados para portugues

### Limitacoes do TextBlob

Durante o desenvolvimento, identificou-se que o TextBlob possui limitacoes significativas:
- **Portugues**: Nao analisa corretamente textos em portugues (retorna sempre neutro/0.0)
- **Contexto**: Nao compreende contexto ou sarcasmo
- **Vocabulario**: Limitado a palavras em ingles

Por essa razao, optei por implementar uma solucao hibrida usando:
1. **LLM (AWS Bedrock)** como metodo principal para maxima precisao
2. **Dicionario customizado** para analise offline confiavel
3. **TextBlob** apenas como fallback final

### Observacao sobre Versao Gratuita

Estou utilizando uma versao gratuita/trial do AWS Bedrock, que pode ter limitacoes de:
- Numero de requisicoes
- Taxa de uso (rate limiting)
- Disponibilidade do servico

Caso o token expire ou falhe, o sistema automaticamente usa o metodo de dicionario, garantindo que a aplicacao continue funcional.

### Resultado da Analise

Independente do metodo utilizado, o resultado sempre retorna:
- **Sentimento**: positivo, negativo ou neutro
- **Pontuacao**: valor entre -1.0 (muito negativo) e 1.0 (muito positivo)
