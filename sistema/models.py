# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

class Repositorio(models.Model):
    url = models.CharField("Url do Repositório:", max_length=100, null=False)
    nome_repositorio = models.CharField("Url do Repositório:", max_length=100, null=False)
    total_projetos = models.IntegerField(null=True)
    data_criacao   = models.DateTimeField(auto_now_add=True)
    proprietario   = models.ForeignKey(User, on_delete=models.CASCADE)

class Projeto(models.Model):
    linguagem      = models.CharField("Projeto:",max_length=100,null=False)
    repositorio    = models.ForeignKey('Repositorio', on_delete=models.CASCADE)
    inserido_em    = models.DateTimeField(auto_now_add=True)
    monitorado     = models.BooleanField(default=True)
