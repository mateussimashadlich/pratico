# Generated by Django 4.0 on 2021-12-21 03:50

from django.db import migrations


def criar_esportes(apps, schema_editor):
    Esporte = apps.get_model('chat', 'Esporte')
    Esporte.objects.create(nome='Basquete')
    Esporte.objects.create(nome='Vôlei')
    Esporte.objects.create(nome='Futebol')
    Esporte.objects.create(nome='Tênis')
    Esporte.objects.create(nome='Calistenia')


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(criar_esportes)
    ]
