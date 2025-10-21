import os
from dotenv import load_dotenv

load_dotenv()


class Configuracao:
    def __init__(self):
        self.token_aws = os.getenv('AWS_BEARER_TOKEN_BEDROCK')
        self.regiao_aws = os.getenv('AWS_REGION', 'us-east-2')
        self.perfil_inferencia = os.getenv('AWS_INFERENCE_PROFILE_ID')

        self.pasta_documentos = 'documentos'
        self.pasta_banco_vetorial = 'banco_vetorial'
        self.tamanho_chunk = 500
        self.sobreposicao_chunk = 50
        self.numero_documentos_relevantes = 3

    def validar(self):
        if not self.token_aws:
            raise ValueError("Token AWS nao configurado no arquivo .env")
        if not self.perfil_inferencia:
            raise ValueError("Perfil de inferencia nao configurado no arquivo .env")
        return True
