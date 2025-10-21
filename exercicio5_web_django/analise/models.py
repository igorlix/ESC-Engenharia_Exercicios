from django.db import models
from django.contrib.auth.models import User


class Analise(models.Model):
    SENTIMENTOS = [
        ('positivo', 'Positivo'),
        ('negativo', 'Negativo'),
        ('neutro', 'Neutro'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='analises')
    texto = models.TextField()
    sentimento = models.CharField(max_length=20, choices=SENTIMENTOS)
    pontuacao = models.FloatField()
    metodo = models.CharField(max_length=50, default='dicionario')
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_criacao']
        verbose_name = 'Análise'
        verbose_name_plural = 'Análises'

    def __str__(self):
        return f"{self.usuario.username} - {self.sentimento} ({self.pontuacao})"
