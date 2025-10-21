from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Analise
from .analisador import AnalisadorSentimento


def registro(request):
    if request.user.is_authenticated:
        return redirect('analise')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('analise')
    else:
        form = UserCreationForm()

    return render(request, 'analise/registro.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('analise')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo, {username}!')
                return redirect('analise')
    else:
        form = AuthenticationForm()

    return render(request, 'analise/login.html', {'form': form})


@login_required
def analise_view(request):
    analisador = AnalisadorSentimento()
    resultado = None

    if request.method == 'POST':
        texto = request.POST.get('texto', '').strip()

        if texto:
            resultado = analisador.analisar(texto)

            Analise.objects.create(
                usuario=request.user,
                texto=texto,
                sentimento=resultado['sentimento'],
                pontuacao=resultado['pontuacao']
            )

            resultado['texto'] = texto
        else:
            messages.error(request, 'Por favor, digite um texto para analisar.')

    historico = Analise.objects.filter(usuario=request.user)[:5]

    return render(request, 'analise/analise.html', {
        'resultado': resultado,
        'historico': historico
    })


def logout_view(request):
    logout(request)
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('login')
