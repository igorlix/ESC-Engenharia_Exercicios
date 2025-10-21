import json
from botocore.exceptions import ClientError


class ExtratorInformacoes:
    def __init__(self, config):
        self.config = config
        self.cliente = config.obter_cliente_bedrock()

    def _criar_prompt_extracao(self, texto_documento):
        prompt = f"""Analise o seguinte documento tecnico e extraia as informacoes solicitadas.

DOCUMENTO:
{texto_documento}

Extraia e estruture as seguintes informacoes em formato JSON:

1. componentes: Lista de componentes mencionados com suas especificacoes
   - nome: nome do componente
   - modelo: modelo ou tipo
   - especificacoes: lista de especificacoes tecnicas relevantes
   - estado: condicao atual (se mencionada)

2. especificacoes_tecnicas: Parametros e valores medidos
   - parametro: nome do parametro
   - valor_medido: valor atual
   - valor_nominal: valor esperado ou normal
   - unidade: unidade de medida
   - status: "normal", "elevado", "reduzido" ou "desconhecido"

3. problemas_relatados: Problemas identificados
   - descricao: descricao do problema
   - componente_afetado: componente relacionado
   - severidade: "critica", "alta", "media", "baixa"
   - impacto: consequencias se nao resolvido

4. acoes_recomendadas: Acoes sugeridas
   - descricao: descricao da acao
   - prioridade: "imediata", "curto_prazo", "medio_prazo", "longo_prazo"
   - prazo: tempo estimado para execucao
   - recursos_necessarios: lista de recursos

5. informacoes_gerais:
   - data: data do relatorio
   - equipamento: identificacao do equipamento
   - local: localizacao
   - responsavel: responsavel tecnico

6. informacoes_ambiguas: Lista de informacoes que estao incompletas ou ambiguas
   - item: descricao do item
   - motivo: por que esta ambiguo ou incompleto
   - sugestao: sugestao de esclarecimento

Retorne APENAS o JSON estruturado, sem texto adicional."""

        return prompt

    def extrair_informacoes(self, texto_documento):
        if not texto_documento:
            return None

        prompt = self._criar_prompt_extracao(texto_documento)

        try:
            corpo_requisicao = {
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "text": prompt
                            }
                        ]
                    }
                ],
                "inferenceConfig": {
                    "temperature": self.config.obter_temperatura()
                }
            }

            resposta = self.cliente.invoke_model(
                modelId=self.config.obter_modelo_id(),
                body=json.dumps(corpo_requisicao)
            )

            corpo_resposta = json.loads(resposta['body'].read())
            texto_resposta = corpo_resposta['output']['message']['content'][0]['text']

            inicio_json = texto_resposta.find('{')
            fim_json = texto_resposta.rfind('}') + 1

            if inicio_json != -1 and fim_json > inicio_json:
                json_extraido = texto_resposta[inicio_json:fim_json]
                dados_estruturados = json.loads(json_extraido)
                return dados_estruturados
            else:
                print("Nao foi possivel encontrar JSON valido na resposta")
                return None

        except ClientError as erro:
            print(f"Erro ao invocar modelo Bedrock: {erro}")
            return None
        except json.JSONDecodeError as erro:
            print(f"Erro ao decodificar JSON: {erro}")
            return None
        except Exception as erro:
            print(f"Erro inesperado: {erro}")
            return None

    def salvar_resultado(self, dados, caminho_saida):
        try:
            with open(caminho_saida, 'w', encoding='utf-8') as arquivo:
                json.dump(dados, arquivo, ensure_ascii=False, indent=2)
            print(f"Resultado salvo em: {caminho_saida}")
            return True
        except Exception as erro:
            print(f"Erro ao salvar resultado: {erro}")
            return False
