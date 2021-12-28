from django.urls import path

from . import views

urlpatterns = [
    path('locais-pratica-esportiva/<int:id_local>', views.LocalPraticaEsportivaCadastroView.as_view(
    ), name='locais_pratica_esportiva'),
    path('locais-pratica-esportiva/', views.LocalPraticaEsportivaCadastroView.as_view(
    ), name='locais_pratica_esportiva'),
    path('locais-pratica-esportiva-list', views.LocalPraticaEsportivaListView.as_view(),
         name='locais_pratica_esportiva_list')
]
