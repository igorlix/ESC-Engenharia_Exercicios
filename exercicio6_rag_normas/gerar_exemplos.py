from src.configuracao import Configuracao
from src.assistente_rag import AssistenteRAG


def gerar_exemplos():
    config = Configuracao()
    config.validar()

    assistente = AssistenteRAG(config)
    assistente.carregar_indice()

    perguntas = [
        "Qual a definição de brinquedo segundo o Inmetro?",
        "Quais são os requisitos de segurança para brinquedos com baterias?",
        "Qual a corrente máxima permitida para plugues de uso doméstico?",
        "Quais são os requisitos de segurança para adaptadores de tomada?",
        "Como deve ser feita a rotulagem de brinquedos segundo o RTQ?",
        "Quais são os limites de substâncias químicas permitidas em brinquedos?",
        "Qual o padrão brasileiro para plugues e tomadas residenciais?",
        "Quais testes mecânicos são obrigatórios para brinquedos?",
    ]

    with open('exemplos_consultas.txt', 'w', encoding='utf-8') as f:
        f.write("EXEMPLOS DE CONSULTAS E RESPOSTAS\n")
        f.write("ASSISTENTE VIRTUAL - NORMAS TECNICAS\n")
        f.write("_" * 80 + "\n\n")

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
