from typing import List
from langchain_core.documents import Document
from .configuracao import Configuracao
from .carregador_documentos import CarregadorDocumentos
from .modelo_embeddings import ModeloEmbeddingsCohereV4, ModeloEmbeddingsAWS, ModeloEmbeddingsTFIDF
from .banco_vetorial import BancoVetorial
from .gerador_respostas import GeradorRespostas


class AssistenteRAG:
    def __init__(self, config: Configuracao):
        self.config = config

        print("Inicializando modelo de embeddings...")

        # Verifica se AWS Embeddings esta configurado
        if config.perfil_inferencia_embeddings:
            try:
                self.modelo_embeddings = ModeloEmbeddingsCohereV4(
                    config.token_aws,
                    config.regiao_aws,
                    config.perfil_inferencia_embeddings
                )
                print(f"Modelo AWS Embeddings carregado: {config.perfil_inferencia_embeddings}")
            except Exception as e:
                print(f"[AVISO] Erro ao carregar AWS Embeddings: {str(e)[:80]}")
                print("Usando TF-IDF como fallback...")
                self.modelo_embeddings = ModeloEmbeddingsTFIDF()
                print("Modelo TF-IDF carregado")
        else:
            self.modelo_embeddings = ModeloEmbeddingsTFIDF()
            print("Modelo TF-IDF carregado (sem AWS configurado)")

        self.banco_vetorial = BancoVetorial(
            config.pasta_banco_vetorial,
            self.modelo_embeddings
        )

        self.gerador_respostas = GeradorRespostas(
            config.token_aws,
            config.regiao_aws,
            config.perfil_inferencia
        )

        self.carregador = CarregadorDocumentos(
            config.pasta_documentos,
            config.tamanho_chunk,
            config.sobreposicao_chunk
        )

    def indexar_documentos(self) -> None:
        print("\n=== Iniciando indexacao de documentos ===\n")

        documentos = self.carregador.processar()

        self.banco_vetorial.criar(documentos)

        print("\n=== Indexacao concluida com sucesso ===\n")

    def carregar_indice(self) -> None:
        print("\n=== Carregando indice existente ===\n")
        self.banco_vetorial.carregar()
        print("Indice carregado com sucesso\n")

    def consultar(self, pergunta: str, mostrar_fontes: bool = True) -> str:
        print(f"\nConsulta: {pergunta}\n")

        documentos_relevantes = self.banco_vetorial.buscar_similares(
            pergunta,
            k=self.config.numero_documentos_relevantes
        )

        if mostrar_fontes:
            print("Documentos relevantes encontrados:")
            for i, doc in enumerate(documentos_relevantes, 1):
                fonte = doc.metadata.get('fonte', 'Desconhecido')
                print(f"  {i}. {fonte}")
            print()

        resposta = self.gerador_respostas.gerar_resposta(pergunta, documentos_relevantes)

        return resposta

    def consultar_interativo(self) -> None:
        print("\n" + "="*60)
        print("ASSISTENTE VIRTUAL - CONSULTA DE NORMAS TECNICAS")
        print("="*60)
        print("\nDigite 'sair' para encerrar\n")

        while True:
            try:
                pergunta = input("Pergunta: ").strip()

                if pergunta.lower() in ['sair', 'exit', 'quit']:
                    print("\nEncerrando assistente...")
                    break

                if not pergunta:
                    continue

                resposta = self.consultar(pergunta)

                print(f"\nResposta:\n{resposta}\n")
                print("-" * 60 + "\n")

            except KeyboardInterrupt:
                print("\n\nEncerrando assistente...")
                break
            except Exception as e:
                print(f"\nErro: {str(e)}\n")
