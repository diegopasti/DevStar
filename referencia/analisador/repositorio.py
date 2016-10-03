# coding: utf-8
'''
Created on 23 de mar de 2016

@author: DIEGOPASTI
'''
from _elementtree import Element
import re
import time
import urllib2

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from referencia.analisador.controle import Controlador


class controle_repositorio():
    
    arquivo     = None 
    link        = None
    controlador = None
    
    def __init__(self):
        #print "Controle de Repositorios construido com sucesso!"
        pass
    
    def baixar_arquivo(self,link):
        conexao = urllib2.urlopen(link)
        self.arquivo = conexao.read()
        
    def simplificar_arquivo(self):
        self.leitor_html = BeautifulSoup(self.arquivo,"html5lib")
        self.arquivo = self.leitor_html.find('div',{'id':'body'})
    
    def get_total_projetos(self):
        self.baixar_arquivo("http://nemo.sonarqube.org/measures/search/68?widget_id=&asc=false&c3_metric=tests&c3_op=eq&cols%5B%5D=metric%3Aalert_status&cols%5B%5D=name&cols%5B%5D=date&cols%5B%5D=metric%3Ancloc&cols%5B%5D=metric%3Aviolations&cols%5B%5D=links&display=list&page=1&pageSize=100&qualifiers%5B%5D=TRK&sort=metric%3Ancloc&id=68")
        self.simplificar_arquivo()
        div = self.arquivo.findAll("div", id="measure_filter_foot_pages")[0].contents[0]
        div = str(div)
        
        resultado = re.search(r'^>*(\d*) results', div).group(1)
        print "Numero de Projetos: ",int(resultado)
        return int(resultado)
                
    def get_links_projetos(self):
        Links = []
        Fonte, Lista = self.get_links("http://nemo.sonarqube.org/measures/search/68?widget_id=&asc=false&c3_metric=tests&c3_op=eq&cols%5B%5D=metric%3Aalert_status&cols%5B%5D=name&cols%5B%5D=date&cols%5B%5D=metric%3Ancloc&cols%5B%5D=metric%3Aviolations&cols%5B%5D=links&display=list&page=1&pageSize=100&qualifiers%5B%5D=TRK&sort=metric%3Ancloc&id=68")
        Links = Links+Lista
        
        while Fonte != None:
            Fonte, Lista = self.get_links(Fonte)
            Links = Links+Lista
        
        dashboards = []
        
        self.controlador = Controlador([])
        for item in Links:   
            url_dash = self.get_dashboard_link(item)
            dashboards.append(url_dash)
            #links_dashboard = self.get_dashboard_link(item)
        
        #print "Olha quantos links consegui: ",len(dashboards)
        self.controlador.encerrar()
        return Links      
        
    def get_links(self,Fonte):
        Links = []
        self.baixar_arquivo(Fonte)
        self.simplificar_arquivo()
                
        div = self.arquivo.findAll("td",{"class":"nowrap"})
                
        for item in div:
            link = item.findAll("a",href=True,title=True)
            if link != []:
                url = "http://nemo.sonarqube.org"+link[0]['href']
                Links.append(url)
                #print "Adicionando link: ",url
                
        footer = self.arquivo.find("tfoot")
       
        list_links = footer.findAll("a",href=True)
        
        url = None
        for link in list_links:
            if "Next" in link:                
                url = "http://nemo.sonarqube.org"+link["href"]
                #print "Adicionando link: ",url
        return url,Links
    
    def get_dashboard_link(self,link):
        dashboard_links = []
        
        """ PEGAR A PAGINA COM O WEBDRIVER """
        
        if self.controlador == None:
            self.controlador = Controlador([])
        self.controlador.iniciar(link)
        #print controlador.driver.page_source
        elementos = self.controlador.driver.find_elements(By.TAG_NAME,"a")
        
        cont = 0
        url_dashboard = ""
        print "Buscando no Link: ",link
        for item in elementos:
            if "is de controle" in item.text:
                if url_dashboard == "":
                    url_dashboard = item.get_attribute("href")
                else:
                    #print "Olha quem eu quero: ",elementos[cont+1].get_attribute("href")
                    url_dashboard = elementos[cont+1].get_attribute("href")
                    break
                
            cont = cont + 1
        
        print "RESPOSTA FINAL: ",url_dashboard
        
        #controlador.carregar_pagina(url_dashboard)
        return url_dashboard
        
        
        """ PEGAR A PAGINA COM URLLIB2
        conexao = urllib2.urlopen(link)
        self.arquivo = conexao.read()
        
        self.leitor_html = BeautifulSoup(self.arquivo,"html5lib")
        self.arquivo = self.leitor_html.find('body')
        #print "Buscando o dashboard de:",link
        print self.arquivo.text
        
        
        elementos = self.arquivo.findAll("a")
        print "Olha quantos elementos tem: ",len(elementos)
        
        for item in elementos:
            print "Olha o link: ",item.text
        """
    
    
    
if __name__=="__main__":
    print "Controle de Repositorio (Teste)"
    repositorio = controle_repositorio()
    #repositorio.get_total_projetos()
    links = repositorio.get_links_projetos()
    print "Olha os links: ",len(links)
    
    repositorio.get_dashboard_link('https://nemo.sonarqube.org/overview?id=963989')
    
        #repositorio.coletar("https://nemo.sonarqube.org/dashboard?id=net.java.openjdk%3Ajdk9&did=1")
        