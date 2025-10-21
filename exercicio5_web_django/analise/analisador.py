from textblob import TextBlob
import unicodedata
import os
import json
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()


class AnalisadorSentimento:
    def __init__(self):
        self.usar_llm = False
        self.cliente_bedrock = None
        self.metodo_usado = 'dicionario'

        token = os.getenv('AWS_BEARER_TOKEN_BEDROCK')
        regiao = os.getenv('AWS_REGION', 'us-east-1')
        self.perfil_inferencia = os.getenv('AWS_INFERENCE_PROFILE_ID')

        if token and self.perfil_inferencia:
            try:
                self.cliente_bedrock = boto3.client(
                    service_name='bedrock-runtime',
                    region_name=regiao,
                    aws_access_key_id=token.split(':')[0] if ':' in token else token,
                    aws_secret_access_key='dummy'
                )
                self.usar_llm = True
            except Exception as e:
                self.usar_llm = False

        self.palavras_positivas = {
            'excelente', 'otimo', 'bom', 'boa', 'maravilhoso', 'fantastico', 'incrivel',
            'perfeito', 'adorei', 'amei', 'feliz', 'alegre', 'satisfeito', 'contente',
            'recomendo', 'legal', 'bacana', 'top', 'show', 'sucesso',
            'eficiente', 'rapido', 'pratico', 'util', 'melhor', 'super', 'positivo',
            'agradavel', 'confortavel', 'bonito', 'lindo', 'formidavel', 'excepcional',
            'brilhante', 'magnifico', 'espetacular', 'sensacional', 'maximo', 'love',
            'excellent', 'good', 'great', 'amazing', 'wonderful', 'perfect', 'best',
            'funciona', 'funcionou', 'aprovado', 'gostei', 'gostoso', 'delicioso'
        }

        self.palavras_negativas = {
            'ruim', 'pessimo', 'horrivel', 'terrivel', 'odiei', 'detestei', 'triste',
            'decepcionante', 'decepcao', 'problema', 'defeito', 'quebrado', 'lento',
            'caro', 'fraco', 'fragil', 'insatisfeito', 'frustrado', 'chato', 'pior',
            'negativo', 'mal', 'dificil', 'complicado', 'desagradavel', 'feio',
            'inutil', 'nunca', 'jamais', 'ineficiente', 'demora', 'lixo', 'erro',
            'bad', 'terrible', 'horrible', 'worst', 'hate', 'awful', 'poor'
        }

    def remover_acentos(self, texto):
        return ''.join(c for c in unicodedata.normalize('NFD', texto)
                      if unicodedata.category(c) != 'Mn')

    def analisar_com_llm(self, texto):
        try:
            prompt = f"""Analise o sentimento do seguinte texto em português e responda APENAS com um JSON no formato exato:
{{"sentimento": "positivo", "pontuacao": 0.85}}

Regras:
- sentimento: deve ser "positivo", "negativo" ou "neutro"
- pontuacao: número decimal entre -1.0 (muito negativo) e 1.0 (muito positivo)
- Use duas casas decimais na pontuação

Texto: {texto}

JSON:"""

            corpo_requisicao = {
                "messages": [
                    {
                        "role": "user",
                        "content": [{"text": prompt}]
                    }
                ],
                "inferenceConfig": {
                    "temperature": 0.1
                }
            }

            resposta = self.cliente_bedrock.invoke_model(
                modelId=self.perfil_inferencia,
                body=json.dumps(corpo_requisicao)
            )

            corpo_resposta = json.loads(resposta['body'].read())
            texto_resposta = corpo_resposta['output']['message']['content'][0]['text']

            inicio_json = texto_resposta.find('{')
            fim_json = texto_resposta.rfind('}') + 1

            if inicio_json != -1 and fim_json > inicio_json:
                json_extraido = texto_resposta[inicio_json:fim_json]
                resultado = json.loads(json_extraido)
                resultado['pontuacao'] = float(resultado['pontuacao'])
                resultado['pontuacao'] = round(max(-1.0, min(1.0, resultado['pontuacao'])), 2)
                resultado['metodo'] = 'llm'
                self.metodo_usado = 'llm'
                return resultado
            else:
                return None

        except Exception:
            return None

    def analisar_com_dicionario(self, texto):
        import re
        texto_normalizado = self.remover_acentos(texto.lower())
        palavras = re.findall(r'\b\w+\b', texto_normalizado)

        pontos_positivos = sum(1 for palavra in palavras if palavra in self.palavras_positivas)
        pontos_negativos = sum(1 for palavra in palavras if palavra in self.palavras_negativas)

        if pontos_positivos == 0 and pontos_negativos == 0:
            try:
                blob = TextBlob(texto)
                polaridade = blob.sentiment.polarity
                metodo = 'textblob'
            except:
                polaridade = 0.0
                metodo = 'textblob'
        else:
            total_palavras_sentimento = pontos_positivos + pontos_negativos
            if total_palavras_sentimento > 0:
                polaridade = (pontos_positivos - pontos_negativos) / total_palavras_sentimento
            else:
                polaridade = 0.0
            metodo = 'dicionario'

        if polaridade > 0.1:
            sentimento = 'positivo'
        elif polaridade < -0.1:
            sentimento = 'negativo'
        else:
            sentimento = 'neutro'

        pontuacao = round(max(-1.0, min(1.0, polaridade)), 2)
        self.metodo_usado = metodo

        return {
            'sentimento': sentimento,
            'pontuacao': pontuacao,
            'metodo': metodo
        }

    def analisar(self, texto):
        if self.usar_llm:
            resultado = self.analisar_com_llm(texto)
            if resultado:
                return resultado

        return self.analisar_com_dicionario(texto)
