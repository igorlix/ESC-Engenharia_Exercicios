import os
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


class CarregadorDocumentos:
    def __init__(self, pasta_documentos: str, tamanho_chunk: int = 500, sobreposicao: int = 50):
        self.pasta_documentos = pasta_documentos
        self.divisor_texto = RecursiveCharacterTextSplitter(
            chunk_size=tamanho_chunk,
            chunk_overlap=sobreposicao,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

    def carregar(self) -> List[Document]:
        documentos = []

        if not os.path.exists(self.pasta_documentos):
            raise FileNotFoundError(f"Pasta {self.pasta_documentos} nao encontrada")

        arquivos = [f for f in os.listdir(self.pasta_documentos)
                   if f.endswith('.txt') or f.endswith('.pdf')]

        if not arquivos:
            raise ValueError(f"Nenhum documento encontrado na pasta {self.pasta_documentos}")

        for arquivo in arquivos:
            caminho_completo = os.path.join(self.pasta_documentos, arquivo)

            if arquivo.endswith('.txt'):
                with open(caminho_completo, 'r', encoding='utf-8') as f:
                    conteudo = f.read()

                documentos.append(Document(
                    page_content=conteudo,
                    metadata={"fonte": arquivo, "tipo": "texto"}
                ))

        print(f"Total de documentos carregados: {len(documentos)}")
        return documentos

    def dividir_documentos(self, documentos: List[Document]) -> List[Document]:
        chunks = self.divisor_texto.split_documents(documentos)

        for i, chunk in enumerate(chunks):
            chunk.metadata['chunk_id'] = i

        print(f"Documentos divididos em {len(chunks)} fragmentos")
        return chunks

    def processar(self) -> List[Document]:
        documentos = self.carregar()
        chunks = self.dividir_documentos(documentos)
        return chunks
