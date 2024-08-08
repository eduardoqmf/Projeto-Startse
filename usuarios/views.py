from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.shortcuts import redirect, render


# Create your views here.
def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR,
                                 'A senha e a confirmação precisam ser iguais')
            return redirect('/usuarios/cadastro')

        if len(senha) < 6:
            messages.add_message(request, constants.ERROR,
                                 'Sua senha deve conter pelo menos 6 dígitos')
            return redirect('/usuarios/cadastro')

        users = User.objects.filter(username=username)

        if users.exists():
            messages.add_message(request, constants.ERROR,
                                 'Já existe um usuário com esse nome')
            return redirect('/usuarios/cadastro')

        user = User.objects.create_user(
            username=username,
            password=senha
        )

        return redirect('/usuarios/login')


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = auth.authenticate(request, username=username, password=senha)

        if user:
            auth.login(request, user)
            return redirect('/empresarios/cadastrar_empresa')  # Vai dar erro

        messages.add_message(request, constants.ERROR,
                             'Usuario ou senha inválidos')
        return redirect('/usuarios/login')
