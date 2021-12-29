from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.urls.base import reverse_lazy
from geopy import distance
from django.forms.models import model_to_dict
from django.views import View
from .forms import LocalPraticaEsportivaForm
from .models import LocalPraticaEsportiva
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.urls import reverse
import requests
# Create your views here.


def index(request):
    return render(request, 'index.html', {})


def room(request, room_name):
    return render(request, 'forum.html', {
        'room_name': room_name
    })


class LocalPraticaEsportivaListView(ListView):
    model = LocalPraticaEsportiva
    template_name = 'locais_pratica_esportiva.html'
    context_object_name = 'locais_pratica_esportiva'

    def get_queryset(self):
        self.queryset = LocalPraticaEsportiva.objects.filter(
            postador=self.request.user)
        return super().get_queryset()


class LocalPraticaEsportivaCadastroView(View):

    def get(self, request, *args, **kwargs):
        id_local = self.kwargs.get('id_local')

        if id_local:
            form = LocalPraticaEsportivaForm(
                instance=LocalPraticaEsportiva.objects.get(pk=id_local, postador=self.request.user))
            url_voltar = reverse('locais_pratica_esportiva_list')
            url_cadastro = reverse('locais_pratica_esportiva', args=[id_local])
            edicao = True

        else:
            form = LocalPraticaEsportivaForm()
            url_voltar = reverse('locais_pratica_esportiva_list')
            url_cadastro = reverse('locais_pratica_esportiva')
            edicao = False

        context = {
            'form_local_pratica_esportiva': form,
            'url_voltar': url_voltar,
            'url_cadastro': url_cadastro,
            'edicao': edicao
        }

        return render(request, 'cadastro.html', context)

    def delete(self, request, *args, **kwargs):
        id_local = self.kwargs.get('id_local')
        LocalPraticaEsportiva.objects.get(
            pk=id_local, postador=self.request.user).delete()

        return JsonResponse({'message': 'Deletado com sucesso.'}, status=204)

    def post(self, request, *args, **kwargs):
        id_local = self.kwargs.get('id_local')
        if id_local:
            local = LocalPraticaEsportiva.objects.get(pk=id_local)
            form = LocalPraticaEsportivaForm(request.POST, instance=local)
        else:
            form = LocalPraticaEsportivaForm(request.POST)
        if form.is_valid():
            endereco = form.cleaned_data['rua'] + \
                ',' + form.cleaned_data['cidade']
            lat_lon = self.get_latitude_longitude_local(endereco)
            if lat_lon != []:
                form.instance.latitude = lat_lon['latitude']
                form.instance.longitude = lat_lon['longitude']
                form.instance.postador = self.request.user
                form.save()
            else:
                context = {
                    'form_local_pratica_esportiva': form,
                    'url_voltar': reverse('locais_pratica_esportiva_list'),
                    'endereco_invalido': True,
                }
                return render(request, 'cadastro.html', context)
        else:
            context = {
                'form_local_pratica_esportiva': form,
                'url_voltar': reverse('locais_pratica_esportiva_list')
            }
            return render(request, 'cadastro.html', context)

        return redirect('locais_pratica_esportiva_list')

    def get_latitude_longitude_local(self, endereco):
        """Obtém latitude e longitude pelo endereço através da API do projeto Nominatim"""

        url = 'https://nominatim.openstreetmap.org/search/' + endereco + '?format=json'
        response = requests.get(url).json()
        if response != []:
            return {'latitude': response[0]["lat"], 'longitude': response[0]["lon"]}

        return []


class LocalPraticaEsportivaDeleteView(DeleteView):
    model = LocalPraticaEsportiva
    success_url = reverse_lazy('locais_pratica_esportiva_list')
