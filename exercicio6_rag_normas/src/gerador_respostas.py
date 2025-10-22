import boto3
import json
from typing import List
from langchain_core.documents import Document


class GeradorRespostas:
    def __init__(self, token: str, regiao: str, perfil_inferencia: str):
        self.cliente = boto3.client(
            service_name='bedrock-runtime',
            region_name=regiao,
            aws_access_key_id=token.split(':')[0] if ':' in token else token,
            aws_secret_access_key='dummy'
        )
        self.perfil_inferencia = perfil_inferencia

    def gerar_resposta(self, pergunta: str, documentos_relevantes: List[Document]) -> str:
        if not documentos_relevantes:
            return "Nao encontrei essa informacao nas normas disponiveis."

        contexto = self._construir_contexto(documentos_relevantes)

        prompt = f"""Voce e um assistente especializado em regulamentos tecnicos do INMETRO.

INSTRUCOES:
1. Analise CUIDADOSAMENTE os documentos fornecidos
2. Responda APENAS com informacoes encontradas nos documentos
3. SEMPRE cite a fonte (nome do arquivo) ao responder
4. Se a informacao NAO estiver nos documentos, responda: "Nao encontrei essa informacao nas normas disponiveis."
5. Seja preciso e direto na resposta

DOCUMENTOS DISPONIVEIS:
{contexto}

PERGUNTA: {pergunta}

RESPOSTA (inclua citacao da fonte):"""

        try:
            corpo_requisicao = {
                "messages": [
                    {
                        "role": "user",
                        "content": [{"text": prompt}]
                    }
                ],
                "inferenceConfig": {
                    "temperature": 0.3,
                    "maxTokens": 1000
                }
            }

            resposta = self.cliente.invoke_model(
                modelId=self.perfil_inferencia,
                body=json.dumps(corpo_requisicao)
            )

            corpo_resposta = json.loads(resposta['body'].read())
            texto_resposta = corpo_resposta['output']['message']['content'][0]['text']

            return texto_resposta.strip()

        except Exception as e:
            return f"Erro ao gerar resposta: {str(e)}"

    def _construir_contexto(self, documentos: List[Document]) -> str:
        contexto_partes = []

        for i, doc in enumerate(documentos, 1):
            fonte = doc.metadata.get('fonte', 'Documento desconhecido')
            conteudo = doc.page_content

            secao = self._extrair_secao(conteudo)

            contexto_partes.append(
                f"[Documento {i}: {fonte}]\n"
                f"[Secao: {secao}]\n"
                f"{conteudo}\n"
            )

        return "\n---\n".join(contexto_partes)

    def _extrair_secao(self, texto: str) -> str:
        linhas = texto.split('\n')
        for linha in linhas:
            if 'Secao' in linha or 'Seção' in linha:
                return linha.strip()
        return "Secao nao identificada"
