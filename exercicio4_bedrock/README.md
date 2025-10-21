# Extrator de Informações de Documentos Técnicos

Aplicação para extração e estruturação automática de informações de documentos técnicos utilizando AWS Bedrock (Claude 3.5 Sonnet).

## Funcionalidades

- Extração automática de componentes mencionados e suas especificações
- Identificação de especificações técnicas e parâmetros medidos
- Detecção de problemas relatados com análise de severidade
- Listagem de ações recomendadas organizadas por prioridade
- Identificação de informações ambíguas ou incompletas
- Exportação dos dados estruturados em formato JSON
- Relatório resumido em console

## Requisitos

- Python 3.8 ou superior
- Conta AWS com acesso ao Amazon Bedrock
- Token de autenticação do Bedrock configurado

## Instalação

```bash
pip install -r requirements.txt
```

## Configuração

### 1. Configurar Token AWS

Configure a variável de ambiente com o token de autenticação do Bedrock:

**Windows (PowerShell):**
```powershell
$env:AWS_BEARER_TOKEN_BEDROCK="seu_token_aqui"
```

**Windows (CMD):**
```cmd
set AWS_BEARER_TOKEN_BEDROCK=seu_token_aqui
```

**Linux/Mac:**
```bash
export AWS_BEARER_TOKEN_BEDROCK="seu_token_aqui"
```

### 2. Região AWS

A aplicação está configurada para usar a região `us-east-2`. Para alterar, modifique o parâmetro `regiao` no código.

## Execução

### Modo Interativo

```bash
python extrator_documentos.py
```

O programa solicitará o caminho do arquivo. Pressione Enter para usar o arquivo de exemplo `documento_tecnico.txt`.

### Uso Programático

```python
from extrator_documentos import ExtratorDocumentosTecnicos

extrator = ExtratorDocumentosTecnicos(regiao='us-east-2')
texto = extrator.carregar_documento('documento_tecnico.txt')
dados = extrator.extrair_informacoes(texto)
extrator.salvar_resultado(dados, 'resultado.json')
```

## Estrutura do JSON de Saída

```json
{
  "informacoes_gerais": {
    "data": "data do relatório",
    "equipamento": "identificação do equipamento",
    "local": "localização",
    "responsavel": "responsável técnico"
  },
  "componentes": [
    {
      "nome": "nome do componente",
      "modelo": "modelo/tipo",
      "especificacoes": ["spec1", "spec2"],
      "estado": "condição atual"
    }
  ],
  "especificacoes_tecnicas": [
    {
      "parametro": "nome do parâmetro",
      "valor_medido": "valor atual",
      "valor_nominal": "valor esperado",
      "unidade": "unidade de medida",
      "status": "normal/elevado/reduzido"
    }
  ],
  "problemas_relatados": [
    {
      "descricao": "descrição do problema",
      "componente_afetado": "componente relacionado",
      "severidade": "critica/alta/media/baixa",
      "impacto": "consequências"
    }
  ],
  "acoes_recomendadas": [
    {
      "descricao": "descrição da ação",
      "prioridade": "imediata/curto_prazo/medio_prazo",
      "prazo": "tempo estimado",
      "recursos_necessarios": ["recurso1", "recurso2"]
    }
  ],
  "informacoes_ambiguas": [
    {
      "item": "descrição do item",
      "motivo": "razão da ambiguidade",
      "sugestao": "sugestão de esclarecimento"
    }
  ]
}
```

## Arquivo de Teste

O arquivo `documento_tecnico.txt` contém um relatório técnico de manutenção de sistema de refrigeração industrial com:

- Informações de equipamento e localização
- Descrição de problemas identificados
- Componentes afetados com especificações
- Diagnóstico preliminar
- Parâmetros técnicos medidos
- Análise de risco
- Ações recomendadas por prioridade
- Recursos necessários

## Mecanismo de Tratamento de Ambiguidades

A aplicação identifica automaticamente informações ambíguas ou incompletas através de:

1. **Análise de contexto**: Identifica valores sem unidades ou especificações incompletas
2. **Verificação de coerência**: Detecta inconsistências entre valores medidos e nominais
3. **Extração de sugestões**: Propõe esclarecimentos para informações ambíguas
4. **Listagem separada**: Organiza itens ambíguos em seção dedicada do JSON

## Saída

A aplicação gera:

1. **Arquivo JSON**: `resultado_extracao_YYYYMMDD_HHMMSS.json` com dados estruturados
2. **Relatório em console**: Resumo com estatísticas e informações principais

## Exemplo de Execução

```
Extrator de Informacoes de Documentos Tecnicos
Utilizando AWS Bedrock - Claude 3.5 Sonnet
--------------------------------------------------------------------------------

Caminho do documento tecnico (ou Enter para usar 'documento_tecnico.txt'):

Carregando documento: documento_tecnico.txt
Documento carregado com sucesso (3542 caracteres)

Extraindo informacoes com AWS Bedrock...
Extracao concluida com sucesso!
Resultado salvo em: resultado_extracao_20240315_143022.json

================================================================================
RELATORIO DE EXTRACAO DE INFORMACOES
================================================================================

INFORMACOES GERAIS:
  data: 15/03/2024
  equipamento: Chiller modelo CFX-5000
  local: Sala de máquinas - Bloco B
  responsavel: Eng. Carlos Silva

COMPONENTES IDENTIFICADOS: 4
  - Compressor scroll modelo CS-750
  - Condensador a água
  - Válvula de expansão eletrônica VEE-40
  - Bomba de água de resfriamento BAR-100

PROBLEMAS RELATADOS: 3
  - [alta] Ruído excessivo durante operação do compressor
  - [critica] Pressão de condensação elevada
  - [alta] Vazão de água de resfriamento reduzida

ACOES RECOMENDADAS: 8
  - [imediata] Reduzir carga térmica para 70% da capacidade
  - [imediata] Verificar e limpar filtro de linha
  - [curto_prazo] Realizar limpeza química do condensador

================================================================================

Dados completos salvos em: resultado_extracao_20240315_143022.json
```

## Observações

- A temperatura do modelo está configurada em 0.1 para respostas mais determinísticas
- O limite de tokens é 4096 para documentos técnicos de tamanho médio
- Para documentos muito grandes, considere dividir em seções
- O modelo Claude 3.5 Sonnet oferece alta precisão na extração de informações técnicas
