from django.contrib import admin
from .models import Analise


@admin.register(Analise)
class AnaliseAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'sentimento', 'pontuacao', 'data_criacao']
    list_filter = ['sentimento', 'data_criacao']
    search_fields = ['usuario__username', 'texto']
    readonly_fields = ['data_criacao']
