# coding: utf-8
'''
Created on 20 de jan de 2016

@author: Diego
'''
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.select import Select

class Controlador():
    
    controle_componentes  = None

    link       = None    
    driver     = None
    componente = None
    
    def __init__(self,extensoes):
        self.carregar_controladores(extensoes)
    
    def iniciar(self,url):
        self.link = url
        self.carregar_pagina(url)
        
    def encerrar(self):
        self.driver.close()
        try:
            alert = self.controlador.driver.switch_to_alert()
            alert.accept()

        except:
            pass

        time.sleep(1)
        try:
            alert = self.controlador.driver.switch_to_alert()
            alert.accept()
        except:
            pass
        
    def carregar_pagina(self,url):
        try:
            self.driver.get(url)
        except:
            print "Falha no carregamento da pagina: ",url
            self.encerrar()
        
    def maximize_window(self):
        self.driver.maximize_window()
    
    def carregar_controladores(self,extensoes):
        try:
            #FIREFOX_PATH = "C:/Program Files (x86)/Mozilla Firefox Ingles/firefox.exe"
            #binary = FirefoxBinary(FIREFOX_PATH)
            #self.driver = webdriver.Firefox(firefox_binary=binary)
            
            profile = webdriver.FirefoxProfile()
            for item in extensoes:
                profile.add_extension(extension=item)
            #driver = webdriver.Firefox()
            self.driver = webdriver.Firefox(firefox_profile=profile)
            #self.driver.maximize_window()
            
        except:
            print "Navegador nao pode ser aberto. Pode ser necessario atualiza-lo antes."
            exit(0)

    def buscar_componente(self,metodo,valor):
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.support.ui import WebDriverWait

        #print "Buscando Elemento: ",valor
        wait = WebDriverWait(self.driver, 5)
        try:
            element = wait.until(EC.element_to_be_clickable((metodo,valor)))
            print "Achei o elemento: ",element
            return element
        except:
            
            time.sleep(2)
            try:
                self.componente = self.driver.find_element(metodo,valor)
                print "Depois Achei o elemento: ",element
                return self.componente
            except:
                #print "Busca por elemento excedeu o tempo maximo.",valor
                return None
    
    def escolher_opcao(self,identificador,opcao):
        self.componente = self.buscar_componente(By.ID,identificador)
        if self.componente != None:
            Select(self.componente).select_by_value(opcao)
            return True
        return False
        
    def selecionar(self,identificador):
        self.componente = self.buscar_componente(By.ID,identificador)
        if self.componente != None:
            try:
                self.componente.click()
                return True
            except:
                #print "Erro! Componente nao pode ser clicado.."
                return False
            
            #try:
                #print "encontrei o componente.. vou tentar clicar",self.componente.text
                
            #    return True
            #except:
            #    print "Componente localizado, mas nao consegui clicar: ",identificador
            #    print "olha o elemento: ",self.componente
            #    self.componente.click()
        return False
    
    def digitar(self,identificador,texto):
        self.componente = self.buscar_componente(By.ID,identificador)
        if self.componente != None:
            self.componente.send_keys(texto)
            return True
        return False
        
    def apagar(self,identificador):
        self.componente = self.buscar_componente(By.ID,identificador)
        if self.componente != None:
            self.componente.clear()
            return True
        return False
    
    def print_screen(self,path):
        self.driver.save_screenshot(path)
