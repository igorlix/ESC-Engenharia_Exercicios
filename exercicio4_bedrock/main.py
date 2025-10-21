from datetime import datetime
from src.config import Config
from src.leitor_documentos import LeitorDocumentos
from src.extrator import ExtratorInformacoes
from src.relatorio import GeradorRelatorio


def main():
    print("Extrator de Informacoes de Documentos Tecnicos")
    print("-" * 80)

    caminho_documento = input("\nCaminho do documento tecnico (ou Enter para usar 'documento_tecnico.txt'): ").strip()

    if not caminho_documento:
        caminho_documento = "documento_tecnico.txt"

    try:
        config = Config()
    except ValueError as erro:
        print(f"Erro de configuracao: {erro}")
        return

    leitor = LeitorDocumentos()
    extrator = ExtratorInformacoes(config)
    gerador_relatorio = GeradorRelatorio()

    print(f"\nCarregando documento: {caminho_documento}")
    texto = leitor.carregar_documento(caminho_documento)

    if not texto:
        print("Erro ao carregar documento. Encerrando.")
        return

    print(f"Documento carregado com sucesso ({len(texto)} caracteres)")
    print("\nExtraindo informacoes...")

    dados_extraidos = extrator.extrair_informacoes(texto)

    if not dados_extraidos:
        print("Erro na extracao de informacoes. Encerrando.")
        return

    print("Extracao concluida com sucesso!")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho_saida = f"resultado_extracao_{timestamp}.json"

    extrator.salvar_resultado(dados_extraidos, caminho_saida)

    gerador_relatorio.gerar_relatorio_resumido(dados_extraidos)

    print(f"Dados completos salvos em: {caminho_saida}")


if __name__ == "__main__":
    main()
