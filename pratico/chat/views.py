import json
import uuid

from django.contrib.auth import authenticate, login, logout
from django.forms.models import model_to_dict
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from geopy import distance
from gerenciamento.models import Esporte, LocalPraticaEsportiva

from .forms import UsuarioForm
from .models import Mensagem


def busca_locais(request):
    return render(request, 'busca.html', {})


def index(request):
    return render(request, 'index.html', {})


class LoginUsuarioView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "usuario/login.html")

    def post(self, request, *args, **kwargs):
        usuario = request.POST['usuario']
        senha = request.POST['senha']
        user = authenticate(request, username=usuario, password=senha)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "usuario/login.html", {'credenciais_invalidas': True})


class LogoutUsuarioView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')


class CadastroUsuarioView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "usuario/cadastro.html", {"form_usuario": UsuarioForm()})

    def post(self, request, *args, **kwargs):
        form_usuario = UsuarioForm(request.POST)
        if form_usuario.is_valid():
            user = form_usuario.save()
            login(request, user)
            return redirect("index")
        else:
            return render(request, "usuario/cadastro.html", {"form_usuario": form_usuario})


class ForumView(View):
    def get(self, request, *args, **kwargs):
        local = LocalPraticaEsportiva.objects.get(pk=kwargs['id_local'])
        esporte = Esporte.objects.get(pk=kwargs['id_esporte'])

        return render(request, 'forum.html', {
            'forum_name': str(uuid.uuid4()),
            'posts': Mensagem.objects.filter(local_pratica_esportiva=local, esporte=esporte),
            'nome_local': local.nome,
            'nome_esporte': esporte.nome,
            'id_local': kwargs['id_local'],
            'id_esporte': kwargs['id_esporte']
        })

    def post(self, request, *args, **kwargs):
        dados_mensagem = json.loads(request.body)
        local_pratica_esportiva = LocalPraticaEsportiva.objects.get(
            pk=dados_mensagem['id_local'])
        esporte = Esporte.objects.get(pk=dados_mensagem['id_esporte'])
        mensagem = Mensagem(texto=dados_mensagem['texto'], local_pratica_esportiva=local_pratica_esportiva,
                            esporte=esporte, enviador=request.user)
        mensagem.save()

        return JsonResponse({'mensagem': 'Mensagem gravada com sucesso.'}, status=200)


class LocalPraticaEsportivaDetailView(DetailView):
    model = LocalPraticaEsportiva
    template_name = 'local_pratica_esportiva.html'
    context_object_name = 'local_pratica_esportiva'


def get_locais_de_pratica_esportiva_proximos(request):
    """Obtém todos os locais de prática esportiva dentro de um raio de 50km"""
    posicao = json.loads(request.body)
    latitude = posicao['latitude']
    longitude = posicao['longitude']

    raio = 50

    locais_pratica_esportiva_no_raio = []
    locais_pratica_esportiva = LocalPraticaEsportiva.objects.all()
    for local in locais_pratica_esportiva:
        distancia = distance.distance(
            (local.latitude, local.longitude), (latitude, longitude)).km

        if distancia <= raio:
            local_dict = model_to_dict(local)
            local_dict.update({'distancia': round(distancia, 1), 'url': reverse(
                'local_pratica_esportiva', args=[local_dict['id']])})
            local_dict.update(
                {'esportes': [esporte.nome for esporte in local_dict['esportes']]})
            locais_pratica_esportiva_no_raio.append(local_dict)

    return JsonResponse({'locais_proximos': locais_pratica_esportiva_no_raio})
