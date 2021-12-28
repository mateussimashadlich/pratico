from django.db import models
from django.contrib.auth import get_user_model


class Esporte(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome


class LocalPraticaEsportiva(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField("Descrição")
    rua = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    esportes = models.ManyToManyField(Esporte, related_name='locais_pratica')
    postador = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
