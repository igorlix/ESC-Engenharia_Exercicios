class LeitorDocumentos:
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
