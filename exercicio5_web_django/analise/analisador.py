from textblob import TextBlob
import unicodedata


class AnalisadorSentimento:
    def __init__(self):
        self.palavras_positivas = {
            'excelente', 'otimo', 'bom', 'boa', 'maravilhoso', 'fantastico', 'incrivel',
            'perfeito', 'adorei', 'amei', 'feliz', 'alegre', 'satisfeito', 'contente',
            'recomendo', 'legal', 'bacana', 'top', 'show', 'sucesso', 'qualidade',
            'eficiente', 'rapido', 'pratico', 'util', 'melhor', 'super', 'positivo',
            'agradavel', 'confortavel', 'bonito', 'lindo', 'formidavel', 'excepcional',
            'brilhante', 'magnifico', 'espetacular', 'sensacional', 'maximo', 'love',
            'excellent', 'good', 'great', 'amazing', 'wonderful', 'perfect', 'best'
        }

        self.palavras_negativas = {
            'ruim', 'pessimo', 'horrivel', 'terrivel', 'odiei', 'detestei', 'triste',
            'decepcionante', 'decepcao', 'problema', 'defeito', 'quebrado', 'lento',
            'caro', 'fraco', 'fragil', 'insatisfeito', 'frustrado', 'chato', 'pior',
            'negativo', 'mal', 'dificil', 'complicado', 'desagradavel', 'feio',
            'inutil', 'nunca', 'jamais', 'ineficiente', 'demora', 'lixo', 'erro',
            'bad', 'terrible', 'horrible', 'worst', 'hate', 'awful', 'poor'
        }

    def remover_acentos(self, texto):
        return ''.join(c for c in unicodedata.normalize('NFD', texto)
                      if unicodedata.category(c) != 'Mn')

    def analisar(self, texto):
        import re
        texto_normalizado = self.remover_acentos(texto.lower())
        palavras = re.findall(r'\b\w+\b', texto_normalizado)

        pontos_positivos = sum(1 for palavra in palavras if palavra in self.palavras_positivas)
        pontos_negativos = sum(1 for palavra in palavras if palavra in self.palavras_negativas)

        if pontos_positivos == 0 and pontos_negativos == 0:
            try:
                blob = TextBlob(texto)
                polaridade = blob.sentiment.polarity
            except:
                polaridade = 0.0
        else:
            total_palavras_sentimento = pontos_positivos + pontos_negativos
            if total_palavras_sentimento > 0:
                polaridade = (pontos_positivos - pontos_negativos) / total_palavras_sentimento
            else:
                polaridade = 0.0

        if polaridade > 0.1:
            sentimento = 'positivo'
        elif polaridade < -0.1:
            sentimento = 'negativo'
        else:
            sentimento = 'neutro'

        pontuacao = round(max(-1.0, min(1.0, polaridade)), 2)

        return {
            'sentimento': sentimento,
            'pontuacao': pontuacao
        }
