from django.shortcuts import render, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import date
from django.http.response import JsonResponse
# Create your views here.

#def index (request) :
#    return redirect('/agenda/')

@login_required(login_url='/login/')
def lista_eventos (request) :
    usuario = request.user
    data_atual = date.today()
    evento = Evento.objects.filter(usuario=usuario, data_evento__gt=data_atual) #__gt == '>'
    dados = {'eventos': evento}
    return render(request, 'agenda.html', dados)

@login_required(login_url='/login/')
def evento (request) :
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render(request, 'evento.html', dados)

@login_required(login_url='/login/')
def submit_evento (request) :
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        usuario = request.user
        id_evento = request.POST.get('id_evento') #o input desse campo não estara visível no html

        if id_evento:  # se o campo escondido do id tiver um id, quer dizer que estou fazendo uma edição
            evento = Evento.objects.get(id=id_evento)
            if evento.usuario == usuario:
                evento.titulo = titulo
                evento.descricao = descricao
                evento.data_evento = data_evento
                evento.save()
            #ou:
            #Evento.objects.filter(id=id_evento).update(titulo=titulo, data_evento=data_evento, descricao=descricao)

        else: # se o campo escondido do id for vazio, que dizer quer estou criando
            Evento.objects.create(titulo=titulo, data_evento=data_evento, descricao=descricao, usuario=usuario)

    return redirect('/')

def login_user (request) :
    return render(request, 'login.html')

def logout_user (request) :
    logout(request)
    return redirect('/')

def submit_login (request) :
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, "Usuário ou senha inválido!")

    return redirect('/')

@login_required(login_url='/login/')
def delete_evento (request, id_evento) :
    usuario = request.user
    evento = Evento.objects.get(id=id_evento)
    if usuario == evento.usuario: # o usuario só exclui o que é dele
        evento.delete()
    return redirect('/')

@login_required(login_url='/login/')
def json_lista_eventos (request):
    usuario = request.user
    evento = Evento.objects.filter(usuario=usuario).values('id','titulo')
    # precisa de safe=false porque esta passando uma lista de dicionarios ao inves de dicionatio direto
    return JsonResponse(list(evento), safe=False)