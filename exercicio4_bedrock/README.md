# Extrator de Informacoes de Documentos Tecnicos

Para a extração e estruturacao das informacoes do documentos utilizei o AWS Bedrock com Amazon Nova Micro. Para acessá-lo criei uma conta gratuita, sem dados bancários válidos, e gerei um token para a API. 

Por essa chave se tratar de um dado sensível (recebi alguns emails da AWS assim que deixei o repositório públco), configurei apenas as permissões necessárias para a chave e limitei a quantidade de consultas para não ultrapassar os créditos da versão gratuita. Se surgir algum problema com o acesso, por favor me contate. 

## Instalacao

```bash
pip install -r requirements.txt
```

### Configuracao

Os dados da API estão no link:

- https://drive.google.com/file/d/1RB3BgLQ8CoeEO7RMkyLKPbjcmzotwz67/view?usp=drive_link

Cole no arquivo .env desse exercício

```
AWS_BEARER_TOKEN_BEDROCK=
AWS_REGION=us-east-2
AWS_INFERENCE_PROFILE_ID=us.amazon.nova-micro-v1:0
```


## Execução

Execute pelo terminal (cmd ou power shell)

```bash
python main.py
```

O programa solicita o caminho do arquivo de entrada. Pressione Enter para usar o arquivo de exemplo `documento_tecnico.txt`.


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

## JSON

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
