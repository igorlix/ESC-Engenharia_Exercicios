from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)


def extrair_emails(texto):
    padrao_email = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(padrao_email, texto)
    return list(set(emails))


@app.route('/api/ex1/extrair-emails', methods=['POST'])
def extrair_emails_endpoint():
    try:
        dados = request.get_json()
        texto = dados.get('texto', '')

        if not texto:
            return jsonify({'erro': 'Texto não fornecido'}), 400

        emails = extrair_emails(texto)

        return jsonify({
            'emails': emails,
            'total': len(emails)
        })

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
