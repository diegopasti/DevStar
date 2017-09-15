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
    projetos       = []

    def __str__(self):
        return self.nome_repositorio

class Projeto(models.Model):
    url_projeto    = models.CharField("Url do Projeto:",max_length=100,null=False,default="")
    nome_projeto   = models.CharField("Projeto:",max_length=100,null=False,default="")
    linguagem      = models.CharField("Linguagem:",max_length=100,null=True)
    repositorio    = models.ForeignKey('Repositorio', on_delete=models.CASCADE)
    inserido_em    = models.DateTimeField(auto_now_add=True)
    monitorado     = models.BooleanField(default=True)
    estado_atual   = None
    estado_anterior = None
    variacao_estado = None
    estados         = []

    def __str__(self):
        return self.nome_projeto

class Estado(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE,default=0)
    linhas_codigo = models.IntegerField(null=True)
    total_linhas = models.IntegerField(null=True)
    arquivos = models.IntegerField(null=True)
    classes = models.IntegerField(null=True)
    metodos = models.IntegerField(null=True)

    complexidade_total = models.DecimalField(max_digits=11, decimal_places=2, null=True)
    complexidade_metodo = models.DecimalField(max_digits=11, decimal_places=2, null=True)
    complexidade_classe = models.DecimalField(max_digits=11, decimal_places=2, null=True)
    complexidade_arquivo = models.DecimalField(max_digits=11, decimal_places=2, null=True)

    taxa_duplicacao = models.DecimalField(max_digits=11, decimal_places=2, null=True)
    taxa_divida_tecnica = models.DecimalField(max_digits=11, decimal_places=2, null=True)

    total_codesmell = models.IntegerField(null=True)

    total_problemas = models.IntegerField(null=True)
    problemas_criticos = models.IntegerField(null=True)
    problemas_importantes = models.IntegerField(null=True)
    problemas_moderados = models.IntegerField(null=True)
    problemas_normais = models.IntegerField(null=True)
    problemas_simples = models.IntegerField(null=True)

    taxa_comentarios = models.DecimalField(max_digits=11, decimal_places=2, null=True)

    ultima_analise = models.DateField(null=True, blank=True)
    data_revisao = models.DateTimeField(auto_now_add=True)

    variacao = []
