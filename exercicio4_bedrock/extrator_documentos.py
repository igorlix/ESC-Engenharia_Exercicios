import json
import os
from datetime import datetime
import boto3
from botocore.exceptions import ClientError


class ExtratorDocumentosTecnicos:

    def __init__(self, regiao='us-east-2'):
        self.regiao = regiao
        self.cliente_bedrock = None
        self.modelo_id = 'us.anthropic.claude-3-5-sonnet-20241022-v2:0'
        self._configurar_cliente()

    def _configurar_cliente(self):
        try:
            token = os.environ.get('AWS_BEARER_TOKEN_BEDROCK')
            if not token:
                raise ValueError("Token AWS_BEARER_TOKEN_BEDROCK nao encontrado nas variaveis de ambiente")

            self.cliente_bedrock = boto3.client(
                service_name='bedrock-runtime',
                region_name=self.regiao,
                aws_access_key_id=token.split(':')[0] if ':' in token else token,
                aws_secret_access_key='dummy'
            )
        except Exception as erro:
            print(f"Erro ao configurar cliente Bedrock: {erro}")
            raise

    def carregar_documento(self, caminho_arquivo):
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                conteudo = arquivo.read()
            return conteudo
        except FileNotFoundError:
            print(f"Arquivo nao encontrado: {caminho_arquivo}")
            return None
        except Exception as erro:
            print(f"Erro ao carregar documento: {erro}")
            return None

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
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4096,
                "temperature": 0.1,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }

            resposta = self.cliente_bedrock.invoke_model(
                modelId=self.modelo_id,
                body=json.dumps(corpo_requisicao)
            )

            corpo_resposta = json.loads(resposta['body'].read())
            texto_resposta = corpo_resposta['content'][0]['text']

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

    def gerar_relatorio_resumido(self, dados):
        print("\n" + "="*80)
        print("RELATORIO DE EXTRACAO DE INFORMACOES")
        print("="*80)

        if 'informacoes_gerais' in dados:
            print("\nINFORMACOES GERAIS:")
            for chave, valor in dados['informacoes_gerais'].items():
                print(f"  {chave}: {valor}")

        if 'componentes' in dados:
            print(f"\nCOMPONENTES IDENTIFICADOS: {len(dados['componentes'])}")
            for comp in dados['componentes']:
                print(f"  - {comp.get('nome', 'N/A')}")

        if 'problemas_relatados' in dados:
            print(f"\nPROBLEMAS RELATADOS: {len(dados['problemas_relatados'])}")
            for prob in dados['problemas_relatados']:
                print(f"  - [{prob.get('severidade', 'N/A')}] {prob.get('descricao', 'N/A')[:60]}...")

        if 'acoes_recomendadas' in dados:
            print(f"\nACOES RECOMENDADAS: {len(dados['acoes_recomendadas'])}")
            for acao in dados['acoes_recomendadas']:
                print(f"  - [{acao.get('prioridade', 'N/A')}] {acao.get('descricao', 'N/A')[:60]}...")

        if 'informacoes_ambiguas' in dados and len(dados['informacoes_ambiguas']) > 0:
            print(f"\nINFORMACOES AMBIGUAS OU INCOMPLETAS: {len(dados['informacoes_ambiguas'])}")
            for item in dados['informacoes_ambiguas']:
                print(f"  - {item.get('item', 'N/A')}")
                print(f"    Motivo: {item.get('motivo', 'N/A')}")

        print("\n" + "="*80 + "\n")


def main():
    print("Extrator de Informacoes de Documentos Tecnicos")
    print("Utilizando AWS Bedrock - Claude 3.5 Sonnet")
    print("-" * 80)

    caminho_documento = input("\nCaminho do documento tecnico (ou Enter para usar 'documento_tecnico.txt'): ").strip()

    if not caminho_documento:
        caminho_documento = "documento_tecnico.txt"

    extrator = ExtratorDocumentosTecnicos(regiao='us-east-2')

    print(f"\nCarregando documento: {caminho_documento}")
    texto = extrator.carregar_documento(caminho_documento)

    if not texto:
        print("Erro ao carregar documento. Encerrando.")
        return

    print(f"Documento carregado com sucesso ({len(texto)} caracteres)")
    print("\nExtraindo informacoes com AWS Bedrock...")

    dados_extraidos = extrator.extrair_informacoes(texto)

    if not dados_extraidos:
        print("Erro na extracao de informacoes. Encerrando.")
        return

    print("Extracao concluida com sucesso!")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho_saida = f"resultado_extracao_{timestamp}.json"

    extrator.salvar_resultado(dados_extraidos, caminho_saida)

    extrator.gerar_relatorio_resumido(dados_extraidos)

    print(f"Dados completos salvos em: {caminho_saida}")


if __name__ == "__main__":
    main()
