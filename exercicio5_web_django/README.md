# Analise de Sentimento Web

Aplicacao web Django para analise de sentimento de textos com sistema de autenticacao.

## Funcionalidades

- Sistema de login e registro de usuarios
- Analise de sentimento de textos (positivo, negativo, neutro)
- Pontuacao numerica da analise
- Historico de analises por usuario
- Interface responsiva com Bootstrap

## Requisitos

- Python 3.8 ou superior

## Instalacao

1. Instale as dependencias:
```bash
pip install -r requirements.txt
```

2. Baixe os dados do TextBlob (necessario apenas na primeira vez):
```bash
python -m textblob.download_corpora
```

3. Execute as migracoes do banco de dados:
```bash
python manage.py migrate
```

4. Crie um superusuario (opcional):
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
- TextBlob (analise de sentimento)
- Bootstrap 5
- SQLite (banco de dados)

## Analise de Sentimento

A analise utiliza a biblioteca TextBlob, que retorna:
- Sentimento: positivo, negativo ou neutro
- Pontuacao: valor entre -1.0 (muito negativo) e 1.0 (muito positivo)
