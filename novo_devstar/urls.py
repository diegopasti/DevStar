"""novo_devstar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^projeto/$', "referencia.views.cadastro_projetos"),
    url(r'^projeto/analisar/$', "referencia.views.coletar_metricas_projetos"),
    url(r'^projeto/(?P<nome_repositorio>[^/]+)/(?P<nome_projeto>[^/]+)$', "referencia.views.visualizar_projeto"),
    url(r'^api/projeto/consultar_metricas/(?P<id_projeto>\d+)/$',"referencia.views.consultar_metricas_projeto"),

    url(r'^login/$', 'sistema.views.login_view'),
    url(r'^logout/$', 'sistema.views.logout_view'),
    url(r'^register/$', 'sistema.views.register_view'),
    url(r'^perfil/$', 'sistema.views.profile_page'),

    #url(r'^perfil/$', 'sistema.views.profile_view'),
    #url(r'^/accounts/login/$', 'sistema.views.login_view'),
    #url(r'^$', "sistema.views.login"),
    url(r'^$', "referencia.views.cadastro_referencias"),
    url(r'^referencia/$', "referencia.views.cadastro_referencias"),
    url(r'^referencia/linguagem/(?P<name>[^/]+)$', "referencia.views.referencia_por_linguagem"),
    url(r'^referencia/atualizar$', "referencia.views.atualizar_referencia"),

    url(r'^api/get_monitored_projects/$', 'sistema.views.get_monitored_projects'),
    url(r'^api/update_project_monitored/$', 'sistema.views.update_project_monitored'),
]
