# Extrator de Informacoes de Documentos Tecnicos

Aplicacao para extracao e estruturacao automatica de informacoes de documentos tecnicos utilizando AWS Bedrock com Amazon Nova Micro via perfil de inferencia.

## Requisitos

- Python 3.8 ou superior
- Conta AWS com acesso ao Amazon Bedrock
- Token Bearer do Bedrock
- Perfil de inferencia configurado no Bedrock

## Instalacao

```bash
pip install -r requirements.txt
```

## Configuracao

1. Copie o arquivo `.env.example` para `.env`:
```bash
cp .env.example .env
```

2. Edite o arquivo `.env` e adicione suas configuracoes AWS:
```
AWS_BEARER_TOKEN_BEDROCK=seu_token_bearer
AWS_REGION=us-east-1
AWS_INFERENCE_PROFILE_ID=us.amazon.nova-micro-v1:0
```

## Execucao

```bash
python main.py
```

O programa solicitara o caminho do arquivo de entrada. Pressione Enter para usar o arquivo de exemplo `documento_tecnico.txt`.

## Estrutura do Projeto

```
exercicio4_bedrock/
├── main.py                      # Arquivo principal de execucao
├── src/
│   ├── config.py                # Configuracao da API
│   ├── leitor_documentos.py     # Leitura de arquivos
│   ├── extrator.py              # Extracao de informacoes
│   └── relatorio.py             # Geracao de relatorios
├── documento_tecnico.txt        # Arquivo de teste
├── requirements.txt             # Dependencias
└── README.md
```

## Funcionalidades

A aplicacao extrai automaticamente:
- Componentes mencionados e suas especificacoes
- Especificacoes tecnicas e parametros medidos
- Problemas relatados com analise de severidade
- Acoes recomendadas organizadas por prioridade
- Informacoes ambiguas ou incompletas

## Saida

A aplicacao gera:
1. Arquivo JSON (`resultado_extracao_YYYYMMDD_HHMMSS.json`) com dados estruturados
2. Relatorio resumido no console

## Esquema JSON

```json
{
  "informacoes_gerais": {
    "data": "data do relatorio",
    "equipamento": "identificacao do equipamento",
    "local": "localizacao",
    "responsavel": "responsavel tecnico"
  },
  "componentes": [
    {
      "nome": "nome do componente",
      "modelo": "modelo/tipo",
      "especificacoes": ["spec1", "spec2"],
      "estado": "condicao atual"
    }
  ],
  "especificacoes_tecnicas": [
    {
      "parametro": "nome do parametro",
      "valor_medido": "valor atual",
      "valor_nominal": "valor esperado",
      "unidade": "unidade de medida",
      "status": "normal/elevado/reduzido/desconhecido"
    }
  ],
  "problemas_relatados": [
    {
      "descricao": "descricao do problema",
      "componente_afetado": "componente relacionado",
      "severidade": "critica/alta/media/baixa",
      "impacto": "consequencias"
    }
  ],
  "acoes_recomendadas": [
    {
      "descricao": "descricao da acao",
      "prioridade": "imediata/curto_prazo/medio_prazo/longo_prazo",
      "prazo": "tempo estimado",
      "recursos_necessarios": ["recurso1", "recurso2"]
    }
  ],
  "informacoes_ambiguas": [
    {
      "item": "descricao do item",
      "motivo": "razao da ambiguidade",
      "sugestao": "sugestao de esclarecimento"
    }
  ]
}
```

## Tratamento de Ambiguidades

A aplicacao identifica automaticamente informacoes ambiguas ou incompletas atraves de analise de contexto, verificacao de coerencia e extracao de sugestoes de esclarecimento.
