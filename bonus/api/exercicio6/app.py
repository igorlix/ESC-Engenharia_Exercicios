from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../exercicio6_rag_normas'))

from src.configuracao import Configuracao
from src.assistente_rag import AssistenteRAG

app = Flask(__name__)
CORS(app)

assistente = None


def inicializar_assistente():
    global assistente
    try:
        config = Configuracao()
        assistente = AssistenteRAG(config)
        assistente.carregar_indice()
        return True
    except Exception as e:
        print(f"Erro ao inicializar assistente: {e}")
        return False


@app.route('/api/ex6/consultar', methods=['POST'])
def consultar_endpoint():
    try:
        if assistente is None:
            return jsonify({'erro': 'Assistente não inicializado'}), 503

        dados = request.get_json()
        pergunta = dados.get('pergunta', '')

        if not pergunta:
            return jsonify({'erro': 'Pergunta não fornecida'}), 400

        resposta = assistente.consultar(pergunta, mostrar_fontes=False)

        return jsonify({'resposta': resposta})

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'assistente_inicializado': assistente is not None
    })


if __name__ == '__main__':
    print("Inicializando assistente RAG...")
    if inicializar_assistente():
        print("Assistente inicializado com sucesso!")
        app.run(host='0.0.0.0', port=5006, debug=False)
    else:
        print("Erro ao inicializar assistente")
