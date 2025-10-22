import os
import shutil
from typing import List
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma


class BancoVetorial:
    def __init__(self, pasta_persistencia: str, modelo_embeddings):
        self.pasta_persistencia = pasta_persistencia
        self.modelo_embeddings = modelo_embeddings
        self.banco = None

    def criar(self, documentos: List[Document]) -> None:
        print("Criando banco vetorial...")

        if os.path.exists(self.pasta_persistencia):
            shutil.rmtree(self.pasta_persistencia)

        self.banco = Chroma.from_documents(
            documents=documentos,
            embedding=self.modelo_embeddings,
            persist_directory=self.pasta_persistencia
        )

        print(f"Banco vetorial criado com {len(documentos)} documentos")

    def carregar(self) -> None:
        if not os.path.exists(self.pasta_persistencia):
            raise FileNotFoundError(
                f"Banco vetorial nao encontrado em {self.pasta_persistencia}. "
                "Execute a indexacao primeiro."
            )

        self.banco = Chroma(
            persist_directory=self.pasta_persistencia,
            embedding_function=self.modelo_embeddings
        )

        print("Banco vetorial carregado com sucesso")

    def buscar_similares(self, consulta: str, k: int = 3) -> List[Document]:
        if not self.banco:
            raise ValueError("Banco vetorial nao inicializado")

        resultados = self.banco.similarity_search(consulta, k=k)
        return resultados

    def buscar_com_score(self, consulta: str, k: int = 3) -> List[tuple]:
        if not self.banco:
            raise ValueError("Banco vetorial nao inicializado")

        resultados = self.banco.similarity_search_with_score(consulta, k=k)
        return resultados
