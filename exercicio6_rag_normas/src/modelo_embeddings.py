from typing import List
import boto3
import json
from langchain.embeddings.base import Embeddings


class ModeloEmbeddingsCohereV4(Embeddings):
    """Modelo Cohere Embed v4 via AWS Bedrock com perfil de inferência"""

    def __init__(self, token: str, regiao: str, perfil_inferencia: str = None):
        self.cliente = boto3.client(
            service_name='bedrock-runtime',
            region_name=regiao,
            aws_access_key_id=token.split(':')[0] if ':' in token else token,
            aws_secret_access_key='dummy'
        )
        # Usa perfil de inferência ou modelo direto
        self.modelo_id = perfil_inferencia if perfil_inferencia else 'cohere.embed-multilingual-v3'
        self.dimensao = 1024  # Cohere Embed v4 retorna 1024 dimensões
        print(f"Inicializado Cohere Embeddings: {self.modelo_id}")

    def gerar_embedding(self, texto: str, input_type: str = "search_document") -> List[float]:
        try:
            corpo_requisicao = {
                "texts": [texto],
                "input_type": input_type,  # "search_document" ou "search_query"
                "embedding_types": ["float"]
            }

            resposta = self.cliente.invoke_model(
                modelId=self.modelo_id,
                body=json.dumps(corpo_requisicao)
            )

            corpo_resposta = json.loads(resposta['body'].read())

            # Cohere retorna lista de embeddings em 'embeddings'
            if 'embeddings' in corpo_resposta and 'float' in corpo_resposta['embeddings']:
                embedding = corpo_resposta['embeddings']['float'][0]
            else:
                # Fallback para estrutura alternativa
                embedding = corpo_resposta.get('embeddings', [[0.0] * self.dimensao])[0]

            return embedding

        except Exception as e:
            print(f"Erro ao gerar embedding Cohere: {str(e)}")
            return [0.0] * self.dimensao

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Gera embeddings para documentos (usa input_type='search_document')"""
        return [self.gerar_embedding(t, input_type="search_document") for t in texts]

    def embed_query(self, text: str) -> List[float]:
        """Gera embedding para query (usa input_type='search_query')"""
        return self.gerar_embedding(text, input_type="search_query")


class ModeloEmbeddingsAWS(Embeddings):
    """Modelo Amazon Titan (fallback se Cohere não funcionar)"""

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
