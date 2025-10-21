from src.configuracao import Configuracao
from src.assistente_rag import AssistenteRAG


def gerar_exemplos():
    config = Configuracao()
    config.validar()

    assistente = AssistenteRAG(config)
    assistente.carregar_indice()

    perguntas = [
        "Qual a secao minima de condutores em circuitos de iluminacao residencial?",
        "Qual a resistencia caracteristica minima fck do concreto para pilares?",
        "Quais os equipamentos de protecao individual obrigatorios em canteiros de obras?",
        "Qual a altura minima para instalacao de tomadas eletricas?",
        "Qual a distancia minima das tomadas em relacao a pontos de agua?",
    ]

    with open('exemplos_consultas.txt', 'w', encoding='utf-8') as f:
        f.write("EXEMPLOS DE CONSULTAS E RESPOSTAS\n")
        f.write("ASSISTENTE VIRTUAL - NORMAS TECNICAS\n")
        f.write("=" * 80 + "\n\n")

        for i, pergunta in enumerate(perguntas, 1):
            print(f"\nProcessando pergunta {i}/{len(perguntas)}...")

            f.write(f"CONSULTA {i}:\n")
            f.write(f"{pergunta}\n\n")

            resposta = assistente.consultar(pergunta, mostrar_fontes=False)

            f.write(f"RESPOSTA {i}:\n")
            f.write(f"{resposta}\n\n")
            f.write("-" * 80 + "\n\n")

    print("\nExemplos gerados com sucesso em 'exemplos_consultas.txt'")


if __name__ == "__main__":
    gerar_exemplos()
