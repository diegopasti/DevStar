# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

class metrica():
    linhas_codigo = "m_ncloc"
    total_linhas = "m_lines"
    arquivos = "m_files"
    classes = "m_classes"
    metodos = "m_functions"

    complexidade_total = "m_complexity"
    complexidade_metodo = "m_function_complexity"
    complexidade_classe = "m_class_complexity"
    complexidade_arquivo = "m_file_complexity"

    taxa_duplicacao = "m_duplicated_lines_density"
    taxa_divida_tecnica = "m_sqale_debt_ratio"
    total_problemas = "m_violations"
    problemas_criticos = "m_blocker_violations"
    problemas_importantes = "m_critical_violations"
    problemas_moderados = "m_major_violations"
    problemas_normais = "m_minor_violations"
    problemas_simples = "m_info_violations"

    code_smell = "m_code_smells"

    taxa_comentarios = "m_comment_lines_density"

class Referencia(models.Model):

    linguagem      = models.CharField("Linguagem:",max_length=100,null=False)
    total_projetos = models.IntegerField(null=True)

    linhas_codigo = models.IntegerField(null=True)
    total_linhas = models.IntegerField(null=True)
    arquivos = models.IntegerField(null=True)
    classes = models.IntegerField(null=True)
    metodos = models.IntegerField(null=True)

    complexidade_total = models.DecimalField(max_digits=11, decimal_places=2,null=True)
    complexidade_metodo = models.DecimalField(max_digits=11, decimal_places=2,null=True)
    complexidade_classe = models.DecimalField(max_digits=11, decimal_places=2,null=True)
    complexidade_arquivo = models.DecimalField(max_digits=11, decimal_places=2,null=True)

    taxa_duplicacao = models.DecimalField(max_digits=11, decimal_places=2,null=True)
    taxa_divida_tecnica = models.DecimalField(max_digits=11, decimal_places=2,null=True)
    total_codesmell = models.IntegerField(null=True,default=0)
    total_problemas = models.IntegerField(null=True)
    problemas_criticos = models.IntegerField(null=True)
    problemas_importantes = models.IntegerField(null=True)
    problemas_moderados = models.IntegerField(null=True)
    problemas_normais = models.IntegerField(null=True)
    problemas_simples = models.IntegerField(null=True)

    taxa_comentarios = models.IntegerField(null=True)
    data_revisao = models.DateTimeField(auto_now_add=True)

    #def __init__(self,nome):
    #    self.linguagem = nome



"""class Repositorio(models.Model):
    url_repositorio =  models.CharField("Repositório:",max_length=100,null=False)

class Projeto(models.Model):
    linguagem      = models.CharField("Projeto:",max_length=100,null=False)
    repositorio    = models.ForeignKey('Manufacturer', on_delete=models.CASCADE)
    inserido_em    = models.DateTimeField(auto_now_add=True)
"""""
class Projeto(models.Model):
    linguagem = models.CharField("Projeto:", max_length=100, null=False)
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

    taxa_comentarios = models.IntegerField(null=True)
    data_revisao = models.DateTimeField(auto_now_add=True)