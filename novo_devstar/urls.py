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
    url(r'^login/$', 'sistema.views.login_view'),
    url(r'^logout/$', 'sistema.views.logout_view'),
    url(r'^register/$', 'sistema.views.register_view'),
    url(r'^perfil/$', 'sistema.views.profile_view'),
    #url(r'^/accounts/login/$', 'sistema.views.login_view'),
    #url(r'^$', "sistema.views.login"),
    url(r'^$', "referencia.views.cadastro_referencias"),
    url(r'^referencia/$', "referencia.views.cadastro_referencias"),
    url(r'^referencia/linguagem/(?P<name>[^/]+)$', "referencia.views.referencia_por_linguagem"),
    url(r'^referencia/atualizar$', "referencia.views.atualizar_referencia"),
]
