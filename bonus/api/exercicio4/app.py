from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)


def obter_cliente_bedrock():
    token = os.getenv('AWS_BEARER_TOKEN_BEDROCK')
    regiao = os.getenv('AWS_REGION', 'us-east-2')

    cliente = boto3.client(
        service_name='bedrock-runtime',
        region_name=regiao,
        aws_access_key_id=token.split(':')[0] if ':' in token else token,
        aws_secret_access_key='dummy'
    )
    return cliente


def extrair_com_bedrock(documento):
    cliente = obter_cliente_bedrock()
    perfil_inferencia = os.getenv('AWS_INFERENCE_PROFILE_ID')

    prompt = f"""Analise o documento abaixo e extraia as seguintes informações em formato JSON:

- titulo: título do documento
- autor: autor(es) do documento
- data: data de criação ou publicação
- secoes: lista de seções principais
- palavras_chave: palavras-chave relevantes
- resumo: resumo breve do conteúdo

Documento:
{documento}

Responda APENAS com o JSON, sem texto adicional.
"""

    corpo_requisicao = {
        "messages": [{"role": "user", "content": [{"text": prompt}]}],
        "inferenceConfig": {"temperature": 0.1, "maxTokens": 2000}
    }

    resposta = cliente.invoke_model(
        modelId=perfil_inferencia,
        body=json.dumps(corpo_requisicao)
    )

    corpo_resposta = json.loads(resposta['body'].read())
    texto_resposta = corpo_resposta['output']['message']['content'][0]['text']

    inicio = texto_resposta.find('{')
    fim = texto_resposta.rfind('}') + 1

    if inicio != -1 and fim > inicio:
        json_extraido = texto_resposta[inicio:fim]
        return json.loads(json_extraido)

    return None


@app.route('/api/ex4/extrair', methods=['POST'])
def extrair_endpoint():
    try:
        dados = request.get_json()
        documento = dados.get('documento', '')

        if not documento:
            return jsonify({'erro': 'Documento não fornecido'}), 400

        resultado = extrair_com_bedrock(documento)

        if resultado:
            return jsonify(resultado)
        else:
            return jsonify({'erro': 'Não foi possível extrair informações'}), 500

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)
