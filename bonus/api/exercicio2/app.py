from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import re
from pathlib import Path

app = Flask(__name__)
CORS(app)

modelo = None
vectorizer = None


def carregar_modelo():
    global modelo, vectorizer

    try:
        modelo_path = Path(__file__).parent / 'modelo_spam.pkl'
        vectorizer_path = Path(__file__).parent / 'vectorizer.pkl'

        if modelo_path.exists() and vectorizer_path.exists():
            with open(modelo_path, 'rb') as f:
                modelo = pickle.load(f)
            with open(vectorizer_path, 'rb') as f:
                vectorizer = pickle.load(f)
            return True
    except:
        pass

    return False


def classificar_regra(mensagem):
    palavras_spam = ['free', 'win', 'winner', 'claim', 'prize', 'congratulations',
                     'urgent', 'call now', 'click here', 'limited time']

    mensagem_lower = mensagem.lower()
    score = sum(1 for palavra in palavras_spam if palavra in mensagem_lower)

    if score >= 3:
        return 'spam', 0.85
    elif score >= 1:
        return 'spam', 0.65
    else:
        return 'ham', 0.70


@app.route('/api/ex2/classificar', methods=['POST'])
def classificar_endpoint():
    try:
        dados = request.get_json()
        mensagem = dados.get('mensagem', '')

        if not mensagem:
            return jsonify({'erro': 'Mensagem não fornecida'}), 400

        if modelo is not None and vectorizer is not None:
            X = vectorizer.transform([mensagem])
            predicao = modelo.predict(X)[0]
            probabilidade = modelo.predict_proba(X)[0]
            confianca = max(probabilidade)
            classificacao = 'spam' if predicao == 1 else 'ham'
        else:
            classificacao, confianca = classificar_regra(mensagem)

        return jsonify({
            'classificacao': classificacao,
            'confianca': float(confianca)
        })

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'modelo_carregado': modelo is not None})


if __name__ == '__main__':
    carregar_modelo()
    app.run(host='0.0.0.0', port=5002, debug=True)
