# Generated by Django 4.0 on 2021-12-21 21:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_alter_localpraticaesportiva_esportes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='localpraticaesportiva',
            name='esportes',
        ),
        migrations.DeleteModel(
            name='Esporte',
        ),
        migrations.DeleteModel(
            name='LocalPraticaEsportiva',
        ),
    ]
