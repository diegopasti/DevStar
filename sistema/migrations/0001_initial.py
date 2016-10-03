# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-20 06:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Repositorio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=100, verbose_name='Url do Reposit\xf3rio:')),
                ('nome_repositorio', models.CharField(max_length=100, verbose_name='Url do Reposit\xf3rio:')),
                ('total_projetos', models.IntegerField(null=True)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('proprietario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
