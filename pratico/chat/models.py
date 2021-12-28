from django.db import models
from gerenciamento.models import LocalPraticaEsportiva, Esporte
from django.contrib.auth import get_user_model


class Mensagem(models.Model):
    data_envio = models.DateTimeField(auto_now=True)
    texto = models.TextField()
    local_pratica_esportiva = models.ForeignKey(
        LocalPraticaEsportiva, on_delete=models.CASCADE)
    esporte = models.ForeignKey(Esporte, on_delete=models.CASCADE)
    enviador = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
