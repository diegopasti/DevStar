# -*- encoding: utf-8 -*-
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from referencia.crowler import coletor_dados
from referencia.models import Referencia
from sistema.models import Projeto, Estado
from django.db.models import Count
from django.db.models.aggregates import Max
from django.contrib.auth.decorators import login_required

from sistema.models import Repositorio
import json

def get_repositorios_usuario(nome):
    nome_usuario = str(nome)
    usuario = User.objects.get(username__exact=nome_usuario)
    meus_repositorios = Repositorio.objects.filter(proprietario=usuario)

    from sistema.models import Projeto
    for item in meus_repositorios:
        item.projetos = Projeto.objects.filter(repositorio=item)

    return meus_repositorios

def get_projetos_usuario(nome):
    nome_usuario = str(nome)
    usuario = User.objects.get(username__exact=nome_usuario)
    meus_repositorios = Repositorio.objects.filter(proprietario=usuario)

    from sistema.models import Projeto
    for item in meus_repositorios:
        item.projetos = Projeto.objects.filter(repositorio=item)

        for projeto in item.projetos:
            estados = Estado.objects.filter(projeto=projeto).order_by('-id')
            projeto.estados = estados

            if len(estados) != 0:
                estado_atual = estados[0]
                projeto.estado_atual = estado_atual

                if len(estados) > 1:
                    projeto.estado_anterior = estados[1]
                    projeto.variacao_estado = calcular_variacao_estado(projeto.estado_anterior,estado_atual)
                else:
                    projeto.estado_anterior = None

            else:
                projeto.estados = []


    return meus_repositorios

def calcular_variacao_estado(estado_anterior,estado_atual):
    estado_variacao = Estado()

    estado_variacao.linhas_codigo  = calcular_diferenca(estado_atual.linhas_codigo,estado_anterior.linhas_codigo)
    estado_variacao.total_linhas   = calcular_diferenca(estado_atual.total_linhas,estado_anterior.total_linhas)
    estado_variacao.arquivos       = calcular_diferenca(estado_atual.arquivos,estado_anterior.arquivos)
    estado_variacao.classes        = calcular_diferenca(estado_atual.classes,estado_anterior.classes)
    estado_variacao.metodos        = calcular_diferenca(estado_atual.metodos,estado_anterior.metodos)

    estado_variacao.complexidade_total   = calcular_diferenca(estado_atual.complexidade_total,estado_anterior.complexidade_total)
    estado_variacao.complexidade_metodo  = calcular_diferenca(estado_atual.complexidade_metodo,estado_anterior.complexidade_metodo)
    estado_variacao.complexidade_classe  = calcular_diferenca(estado_atual.complexidade_classe,estado_anterior.complexidade_classe)
    estado_variacao.complexidade_arquivo = calcular_diferenca(estado_atual.complexidade_arquivo,estado_anterior.complexidade_arquivo)

    estado_variacao.taxa_duplicacao     = calcular_diferenca(estado_atual.taxa_duplicacao,estado_anterior.taxa_duplicacao)
    estado_variacao.taxa_divida_tecnica = calcular_diferenca(estado_atual.taxa_divida_tecnica,estado_anterior.taxa_divida_tecnica)

    estado_variacao.total_problemas       = calcular_diferenca(estado_atual.total_problemas,estado_anterior.total_problemas)
    estado_variacao.problemas_criticos    = calcular_diferenca(estado_atual.problemas_criticos,estado_anterior.problemas_criticos)
    estado_variacao.problemas_importantes = calcular_diferenca(estado_atual.problemas_importantes,estado_anterior.problemas_importantes)
    estado_variacao.problemas_moderados   = calcular_diferenca(estado_atual.problemas_moderados,estado_anterior.problemas_moderados)
    estado_variacao.problemas_normais     = calcular_diferenca(estado_atual.problemas_normais,estado_anterior.problemas_normais)
    estado_variacao.problemas_simples     = calcular_diferenca(estado_atual.problemas_simples,estado_anterior.problemas_simples)

    estado_variacao.total_codesmell       = calcular_diferenca(estado_atual.total_codesmell,estado_anterior.total_codesmell)
    estado_variacao.taxa_comentarios      = calcular_diferenca(estado_atual.taxa_comentarios,estado_anterior.taxa_comentarios)
    return estado_variacao

def calcular_diferenca(numerador,divisor):
    if divisor != 0:
        if type(numerador) == int:
            numerador = float(numerador)

        return round((numerador / divisor) * 100 - 100,2)
    else:
        return numerador

def referencia_por_linguagem(request,name):
    lista_referencias = Referencia.objects.filter(linguagem=name.upper())
    linguagens_projetos = Referencia.objects.values('linguagem').annotate(projetos=Max('total_projetos'))

    meus_respositorios = get_repositorios_usuario(str(request.user))

    return render_to_response("referencia/referencia_por_linguagem.html",
                              {'dados': lista_referencias,'linguagem':name.upper(),'meus_repositorios':meus_respositorios, 'linguagens_projetos': linguagens_projetos},
                              context_instance=RequestContext(request))

@login_required
def cadastro_referencias(request):
    erro = False
    #lista_referencias = Referencia.objects.values('linguagem').annotate(Max('data_revisao'))

    #lista_referencias = Referencia.objects.values().annotate(latest_date=Max('data_revisao'))

    #lista_referencias = Referencia.objects.order_by('linguagem', 'data_revisao').distinct('linguagem')#.annotate(Max('linguagem__data_revisao'))


    #max_date = Referencia.objects.latest('data_revisao').data_revisao
    #print "Olha a data da ultima revisao: ",max_date
    #lista_referencias = Referencia.objects.filter(data_revisao__startswith=max_date)

    numero_linguagens = len(Referencia.objects.values('linguagem').distinct())
    lista_referencias = Referencia.objects.all().order_by('-data_revisao')[:numero_linguagens]

    meus_respositorios = get_repositorios_usuario(str(request.user))
    linguagens_projetos = Referencia.objects.values('linguagem').annotate(projetos=Max('total_projetos'))

    #print linguagens_projetos
    print "Veja quantas referencias temos:",lista_referencias
    return render_to_response("referencia/cadastro.html",
                              {'dados': lista_referencias,'meus_repositorios':meus_respositorios,'linguagens_projetos':linguagens_projetos},
                              context_instance=RequestContext(request))

def cadastro_projetos(request):
    erro = False
    #numero_linguagens = len(Referencia.objects.values('linguagem').distinct())

    #lista_referencias = Referencia.objects.all().order_by('-data_revisao')[:numero_linguagens]


    #linguagens_projetos = Referencia.objects.values('linguagem').annotate(projetos=Max('total_projetos'))

    lista_projetos = Projeto.objects.all()
    meus_respositorios = get_projetos_usuario(str(request.user))
    linguagens_projetos = Referencia.objects.values('linguagem').annotate(projetos=Max('total_projetos'))

    #print linguagens_projetos
    print "Veja quantas referencias temos:",meus_respositorios
    return render_to_response("projeto/cadastro.html",
                              {'meus_repositorios': meus_respositorios,'linguagens_projetos':linguagens_projetos},
                              context_instance=RequestContext(request))

def consultar_metricas_projeto(request,id_projeto):
    # if True: #request.is_ajax()
    estado = Estado.objects.filter(projeto_id=int(id_projeto)).latest('id')
    projeto = Projeto.objects.get(pk=int(id_projeto))
    referencia = Referencia.objects.filter(linguagem=projeto.linguagem).last()# values(projeto.linguagem).annotate(projetos=Max('total_projetos'))
    dados = []
    response_dict = {}
    response_dict.update(serializar_resumo_metricas('complexidade', estado.complexidade_metodo, referencia.complexidade_metodo).items())
    response_dict.update(serializar_resumo_metricas('duplicacao', estado.taxa_duplicacao, referencia.taxa_duplicacao).items())
    response_dict.update(serializar_resumo_metricas('divida_tecnica', estado.taxa_divida_tecnica, referencia.taxa_divida_tecnica).items())
    response_dict.update(serializar_resumo_metricas('comentarios', estado.taxa_comentarios,referencia.taxa_comentarios).items())
    response_dict.update(serializar_resumo_metricas('codesmell', estado.total_codesmell, 0).items())

    """response_dict['complexidade_projeto'] = float(estado.complexidade_metodo)
    response_dict['complexidade_global'] =  float(referencia.complexidade_metodo)

    if response_dict['complexidade_projeto'] < response_dict['complexidade_global']:
        response_dict['complexidade_percentual'] = "%.2f"%(round(float(estado.complexidade_metodo) / float(referencia.complexidade_metodo), 2) * 100)
        response_dict['complexidade_resultado'] = True
    else:
        response_dict['complexidade_percentual'] = "%.2f"%(100)
        response_dict['complexidade_resultado'] = False

    response_dict['duplicacao_projeto'] = float(estado.taxa_duplicacao)
    response_dict['duplicacao_global']  = float(referencia.taxa_duplicacao)

    if response_dict['duplicacao_projeto'] < response_dict['duplicacao_global']:
        response_dict['duplicacao_percentual'] = "%.2f"%(round(float(estado.taxa_duplicacao) / float(referencia.taxa_duplicacao), 2) * 100)
        response_dict['duplicacao_resultado'] = True
    else:
        response_dict['duplicacao_resultado'] = False
        response_dict['duplicacao_percentual'] = "%.2f" % (100)

    response_dict['divida_tecnica_projeto'] = float(estado.taxa_divida_tecnica)
    response_dict['divida_tecnica_global'] = float(referencia.taxa_divida_tecnica)
    if response_dict['divida_tecnica_projeto'] < response_dict['divida_tecnica_global']:
        response_dict['divida_tecnica_resultado'] = True
        response_dict['divida_tecnica_percentual'] = "%.2f"%(round(float(estado.taxa_divida_tecnica) / float(referencia.taxa_divida_tecnica), 2) * 100)
    else:
        response_dict['divida_tecnica_percentual'] = "%.2f"%(100)
        response_dict['divida_tecnica_resultado'] = False
    """

    data = json.dumps(response_dict)
    return HttpResponse(data, content_type='application/json')
    # else:
    # raise Http404

def serializar_resumo_metricas(metrica,valor_projeto,valor_global):
    response_dict = {}
    response_dict[metrica+'_projeto'] = float(valor_projeto)
    response_dict[metrica+'_global'] = float(valor_global)

    if response_dict[metrica+'_projeto'] < response_dict[metrica+'_global']:
        response_dict[metrica+'_percentual'] = "%.2f" % (round(float(valor_projeto) / float(valor_global), 2) * 100)
        response_dict[metrica+'_resultado'] = True
    else:
        response_dict[metrica+'_percentual'] = "%.2f" % (100)
        response_dict[metrica+'_resultado'] = False
    return response_dict


class VariacaoEstado:

    def __init__(self,estado_atual,estado_anterior):
        self.estado_atual = estado_atual
        self.estado_anterior = estado_anterior
        self.variacao = self.criar_variacao()

    def comparar_versoes(self):
        versao_diferente = False
        for item in self.estado_atual.__dict__:
            if item[0] != '_' and item != 'id' and item != 'data_revisao' and item != 'ultima_analise':
                primeiro_valor = self.estado_atual.__dict__[item]
                segundo_valor = self.estado_anterior.__dict__[item]
                if 'Decimal' in str(type(self.estado_anterior.__dict__[item])):
                    segundo_valor = round(float(self.estado_anterior.__dict__[item]),2)
                    primeiro_valor = round(float(self.estado_atual.__dict__[item]),2)

                if(primeiro_valor != segundo_valor):
                    #print("ATRIBUTOS NAO SAO IGUAIS: ",self.estado_anterior.__dict__['projeto_id'], item, primeiro_valor, segundo_valor)
                    versao_diferente = True
                    break
        return versao_diferente

    def criar_variacao(self):
        variacao = Estado()
        if self.estado_anterior is not None:
            variacao.total_problemas = self.calcular_variacao(self.estado_atual.total_problemas, self.estado_anterior.total_problemas)
            variacao.problemas_criticos = self.calcular_variacao(self.estado_atual.problemas_criticos, self.estado_anterior.problemas_criticos)
            variacao.problemas_importantes = self.calcular_variacao(self.estado_atual.problemas_importantes,self.estado_anterior.problemas_importantes)
            variacao.problemas_moderados = self.calcular_variacao(self.estado_atual.problemas_moderados,self.estado_anterior.problemas_moderados)
            #print("VEJA: ",self.estado_atual.problemas_normais,self.estado_atual.problemas_simples, self.estado_anterior.problemas_normais,self.estado_anterior.problemas_simples)
            variacao.problemas_normais = self.calcular_variacao(self.estado_atual.problemas_normais+self.estado_atual.problemas_simples, self.estado_anterior.problemas_normais+self.estado_anterior.problemas_simples)
            #print("VEJA ENTAO A VARIACAO: ",variacao.problemas_normais)
        else:
            variacao.total_problemas = None
            variacao.problemas_criticos = None
            variacao.problemas_importantes = None
            variacao.problemas_moderados = None
            variacao.problemas_normais = None

        return variacao

    def calcular_variacao(self,metrica_atual, metrica_anterior):
        metrica_anterior = float(metrica_anterior)
        metrica_atual = float(metrica_atual)

        if metrica_anterior != 0 and metrica_anterior is not None:
            valor = (metrica_anterior-metrica_atual)#/metrica_anterior
            if(valor < 0):
                valor = valor *(-1)
            return round(((valor)/metrica_anterior)*100,2)
        else:
            return None



def visualizar_projeto(request,nome_repositorio,nome_projeto):
    usuario = User.objects.get(username__exact=str(request.user))
    meus_repositorios = Repositorio.objects.filter(proprietario=usuario)
    repositorio = meus_repositorios.get(nome_repositorio__exact=nome_repositorio.upper())
    projeto = Projeto.objects.filter(repositorio=repositorio).get(nome_projeto__exact=nome_projeto.upper())
    referencia = Referencia.objects.filter(linguagem=projeto.linguagem.upper()).last()
    revisoes = Estado.objects.filter(projeto=projeto).order_by('-data_revisao')
    linguagens_projetos = Referencia.objects.values('linguagem').annotate(projetos=Max('total_projetos'))
    meus_respositorios = get_repositorios_usuario(str(request.user))

    referencia.complexidade_metodo = round(float(referencia.complexidade_total)/referencia.metodos,2) #comentario_over_referencia
    referencia.save()

    complexidade_over_referencia = str(round((float(revisoes.last().complexidade_metodo) / referencia.complexidade_metodo) * 100,2))  # float((revisoes.last().taxa_comentarios)/referencia.taxa_comentarios)*100, 2)
    comentario_over_referencia = str(round((float(revisoes.last().taxa_comentarios) / referencia.taxa_comentarios) * 100,2))  # float((revisoes.last().taxa_comentarios)/referencia.taxa_comentarios)*100, 2)
    #print "Olha o rate:",referencia.complexidade_metodo

    revisoes = list(revisoes)
    if len(revisoes) > 1:
        variacao_estado = VariacaoEstado(revisoes[-2],revisoes[-1])
    else:
        variacao_estado = VariacaoEstado(revisoes[-1], None)

    return render_to_response("projeto/projeto.html",
                              {'dados': [],
                               'repositorio':repositorio.nome_repositorio,
                               'projeto': projeto,

                               'meus_repositorios': meus_respositorios,
                               'linguagens_projetos': linguagens_projetos,

                               'estados_projeto': revisoes,
                               'estado_atual': variacao_estado,
                               'referencia':referencia,

                               'complexidade_over_referencia':complexidade_over_referencia,
                               'comentario_over_referencia':comentario_over_referencia

                               },
                              context_instance=RequestContext(request))

def coletar_metricas_projetos_manual(usuario):
    meus_respositorios = get_repositorios_usuario(usuario)
    lista_revisoes = []
    for item in meus_respositorios:
        estados = coletor_dados().coletar_metricas_projetos(item)
        lista_revisoes.append(estados)
    return lista_revisoes

def coletar_metricas_projetos(request):
    if request.is_ajax():
        meus_respositorios = get_repositorios_usuario(str(request.user))
        lista_revisoes = []
        for item in meus_respositorios:
            estados = coletor_dados().coletar_metricas_projetos(item)

        #for item in lista_referencias:
        #    item.save()

        response_dict = {}
        response_dict['success'] = True

        data = json.dumps(response_dict)
        return HttpResponse(data)

def atualizar_referencia(request):
    if request.is_ajax():
        lista_referencias = coletor_dados().coletar_referencias()

        for item in lista_referencias:
            item.save()

        data = ""
        #data = json.dumps(resultado)
        return HttpResponse(data)


    """
    formulario = formulario_adicionar_documento()

    if (request.method == "POST"):
        formulario = formulario_adicionar_documento(request.POST)

        if 'adicionar_documento' in request.POST:

            if formulario.is_valid():
                doc = documento()
                doc.nome = formulario['documento'].value().upper()
                doc.descricao = formulario['descricao'].value()
                doc.save()
                formulario = formulario_adicionar_documento()
                messages.add_message(request, messages.SUCCESS, "Inclusão Realizada com sucesso!")

            else:
                messages.add_message(request, messages.SUCCESS, "Erro! Inclusão não pode ser realizada!")
                erro = True

        elif 'alterar_documento' in request.POST:
            id_documento = int(request.POST['alterar_documento'])
            doc = documento.objects.get(pk=id_documento)
            doc.nome = formulario['documento'].value().upper()
            doc.descricao = formulario['descricao'].value()
            doc.save()
            formulario = formulario_adicionar_documento()
            messages.add_message(request, messages.SUCCESS, "Alteração realizada com sucesso!")

        else:
            pass

    return render_to_response("protocolo/cadastro.html",
                              {'dados': documentos,'formulario':formulario,'erro':erro},
                              context_instance=RequestContext(request))


def get_documento(request, id):
    doc = documento.objects.get(pk=id)
    if doc != None:
        resultado = [doc.nome,doc.descricao]
    else:
        resultado = ["", ""]
        raise Http404

    data = json.dumps(resultado)
    return HttpResponse(data, content_type='application/json')

def excluir_documento(request, id):
    doc = documento.objects.get(pk=id)
    try:
        doc.delete()
        resultado = ["SUCESS"]
    except:
        resultado = ["ERROR"]
        raise Http404

    data = json.dumps(resultado)
    return HttpResponse(data, content_type='application/json')
"""