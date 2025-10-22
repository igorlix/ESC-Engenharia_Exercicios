import os
import boto3
from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self):
        self.token = os.getenv('AWS_BEARER_TOKEN_BEDROCK')
        self.regiao = os.getenv('AWS_REGION', 'us-east-2')
        self.perfil_inferencia = os.getenv('AWS_INFERENCE_PROFILE_ID')

        if not self.token:
            raise ValueError("AWS_BEARER_TOKEN_BEDROCK nao encontrada no arquivo .env")

        if not self.perfil_inferencia:
            raise ValueError("AWS_INFERENCE_PROFILE_ID deve estar no arquivo .env")

        self.temperatura = 0.1
        self.max_tokens = 4096

    def obter_cliente_bedrock(self):
        cliente = boto3.client(
            service_name='bedrock-runtime',
            region_name=self.regiao,
            aws_access_key_id=self.token.split(':')[0] if ':' in self.token else self.token,
            aws_secret_access_key='dummy'
        )
        return cliente

    def obter_modelo_id(self):
        return self.perfil_inferencia

    def obter_temperatura(self):
        return self.temperatura

    def obter_max_tokens(self):
        return self.max_tokens
