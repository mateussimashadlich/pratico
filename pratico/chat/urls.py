from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('busca', views.busca_locais, name='busca'),
    path('locais-pratica-esportiva-proximos', views.get_locais_de_pratica_esportiva_proximos,
         name="locais_pratica_esportiva_proximos"),
    path('local-pratica-esportiva/<pk>', views.LocalPraticaEsportivaDetailView.as_view(),
         name='local_pratica_esportiva'),
    path('chat/<int:id_local>/<int:id_esporte>',
         views.ChatView.as_view(), name='chat'),
    path('login', views.LoginUsuarioView.as_view(), name='login'),
    path('usuario/cadastro', views.CadastroUsuarioView.as_view(),
         name='cadastro_usuario'),
]
