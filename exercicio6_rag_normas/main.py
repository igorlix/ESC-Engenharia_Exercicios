import sys
from src.configuracao import Configuracao
from src.assistente_rag import AssistenteRAG


def main():
    try:
        config = Configuracao()
        config.validar()

        assistente = AssistenteRAG(config)

        if len(sys.argv) > 1 and sys.argv[1] == 'indexar':
            assistente.indexar_documentos()
            print("\nDocumentos indexados com sucesso!")
            print("Execute 'python main.py' para iniciar o assistente de consultas")

        else:
            assistente.carregar_indice()
            assistente.consultar_interativo()

    except FileNotFoundError as e:
        print(f"\nErro: {e}")
        print("\nExecute primeiro: python main.py indexar")
    except ValueError as e:
        print(f"\nErro de configuracao: {e}")
        print("\nVerifique o arquivo .env com as credenciais AWS")
    except Exception as e:
        print(f"\nErro inesperado: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
