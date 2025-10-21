from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Analise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField()),
                ('sentimento', models.CharField(choices=[('positivo', 'Positivo'), ('negativo', 'Negativo'), ('neutro', 'Neutro')], max_length=20)),
                ('pontuacao', models.FloatField()),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='analises', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Análise',
                'verbose_name_plural': 'Análises',
                'ordering': ['-data_criacao'],
            },
        ),
    ]
