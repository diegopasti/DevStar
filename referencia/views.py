# -*- encoding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from referencia.crowler import coletor_dados
from referencia.models import Referencia, Projeto
from django.db.models import Count
from django.db.models.aggregates import Max
from django.contrib.auth.decorators import login_required

def referencia_por_linguagem(request,name):
    lista_referencias = Referencia.objects.filter(linguagem=name.upper())
    linguagens_projetos = Referencia.objects.values('linguagem').annotate(projetos=Max('total_projetos'))
    return render_to_response("referencia/referencia_por_linguagem.html",
                              {'dados': lista_referencias, 'linguagens_projetos': linguagens_projetos},
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


    linguagens_projetos = Referencia.objects.values('linguagem').annotate(projetos=Max('total_projetos'))

    #print linguagens_projetos
    print "Veja quantas referencias temos:",lista_referencias
    return render_to_response("referencia/cadastro.html",
                              {'dados': lista_referencias,'linguagens_projetos':linguagens_projetos},
                              context_instance=RequestContext(request))


def cadastro_projetos(request):
    erro = False
    #numero_linguagens = len(Referencia.objects.values('linguagem').distinct())

    #lista_referencias = Referencia.objects.all().order_by('-data_revisao')[:numero_linguagens]


    #linguagens_projetos = Referencia.objects.values('linguagem').annotate(projetos=Max('total_projetos'))

    lista_projetos = Projeto.objects.all()

    #print linguagens_projetos
    print "Veja quantas referencias temos:",lista_projetos
    return render_to_response("referencia/cadastro.html",
                              {'dados': lista_projetos,'linguagens_projetos':[]},
                              context_instance=RequestContext(request))


def coletar_metricas_projetos(request):
    if request.is_ajax():
        lista_referencias = coletor_dados().coletar_metricas_projetos()

        #for item in lista_referencias:
        #    item.save()

        #data = ""
        # data = json.dumps(resultado)
        #return HttpResponse(data)


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