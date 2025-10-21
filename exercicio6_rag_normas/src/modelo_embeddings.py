from typing import List
import boto3
import json
from langchain.embeddings.base import Embeddings


class ModeloEmbeddingsAWS(Embeddings):
    def __init__(self, token: str, regiao: str):
        self.cliente = boto3.client(
            service_name='bedrock-runtime',
            region_name=regiao,
            aws_access_key_id=token.split(':')[0] if ':' in token else token,
            aws_secret_access_key='dummy'
        )
        self.modelo_id = 'amazon.titan-embed-text-v1'
        self.dimensao = 1536

    def gerar_embedding(self, texto: str) -> List[float]:
        try:
            corpo_requisicao = json.dumps({"inputText": texto})

            resposta = self.cliente.invoke_model(
                modelId=self.modelo_id,
                body=corpo_requisicao
            )

            corpo_resposta = json.loads(resposta['body'].read())
            embedding = corpo_resposta['embedding']

            return embedding

        except Exception as e:
            print(f"Erro ao gerar embedding: {str(e)}")
            return [0.0] * self.dimensao

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self.gerar_embedding(t) for t in texts]

    def embed_query(self, text: str) -> List[float]:
        return self.gerar_embedding(text)


class ModeloEmbeddingsTFIDF(Embeddings):
    """Modelo baseado em TF-IDF para fallback (sem download de modelos)"""

    def __init__(self):
        from sklearn.feature_extraction.text import TfidfVectorizer
        import numpy as np

        self.vectorizer = TfidfVectorizer(max_features=384, ngram_range=(1, 2))
        self.corpus_fitted = False
        self.dimensao = 384

    def _preparar_texto(self, texto: str) -> str:
        return texto.lower()

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        texts_processados = [self._preparar_texto(t) for t in texts]

        if not self.corpus_fitted:
            self.vectorizer.fit(texts_processados)
            self.corpus_fitted = True

        matriz = self.vectorizer.transform(texts_processados)
        return matriz.toarray().tolist()

    def embed_query(self, text: str) -> List[float]:
        texto_processado = self._preparar_texto(text)

        if not self.corpus_fitted:
            return [0.0] * self.dimensao

        vetor = self.vectorizer.transform([texto_processado])
        return vetor.toarray()[0].tolist()
