'''
Created on 7 de mar de 2016

@author: DIEGOPASTI
'''
import re
import urllib2
from bs4 import BeautifulSoup

from referencia.models import Referencia, metrica

class coletor_dados():
    
    arquivo = None 
    link    = None
    
    #def __init__(self):
    #    print "Coletor construido com sucesso!"
    
    def baixar_arquivo(self,link):
        conexao = urllib2.urlopen(link)
        self.arquivo = conexao.read()
        self.simplificar_arquivo()
        
    def simplificar_arquivo(self):
        self.leitor_html = BeautifulSoup(self.arquivo,"html5lib")
        self.arquivo = self.leitor_html.find('div',{'id':'body'})

    def coletar_metricas_projetos(self):
        resumo_page = "http://localhost:9000/measures/search/1?asc=true&cols%5B%5D=metric%3Aalert_status&cols%5B%5D=name&cols%5B%5D=metric%3Alines&cols%5B%5D=metric%3Ancloc&cols%5B%5D=metric%3Afunction_complexity&cols%5B%5D=metric%3Aclass_complexity&cols%5B%5D=metric%3Afile_complexity&cols%5B%5D=metric%3Acomment_lines_density&cols%5B%5D=metric%3Aduplicated_lines_density&cols%5B%5D=metric%3Aviolations&cols%5B%5D=metric%3Ablocker_violations&cols%5B%5D=metric%3Acritical_violations&cols%5B%5D=metric%3Amajor_violations&cols%5B%5D=metric%3Aminor_violations&cols%5B%5D=metric%3Ainfo_violations&cols%5B%5D=metric%3Asqale_index&cols%5B%5D=metric%3Asqale_debt_ratio&cols%5B%5D=metric%3Acode_smells&display=list&pageSize=100&qualifiers=TRK&sort=name&id=1&edit=true"
        self.baixar_arquivo(resumo_page)
        registros = self.get_registros()
        for item in registros:
            print item

    def coletar_referencias(self):
        base_url = "https://sonarqube.com/measures/search/99?base=Languages"
        resumo_page = "https://sonarqube.com/measures/search/99?asc=true&base=Languages&cols%5B%5D=name&cols%5B%5D=date&cols%5B%5D=metric%3Alines&cols%5B%5D=metric%3Ancloc&cols%5B%5D=metric%3Aviolations&cols%5B%5D=metric%3Aprojects&cols%5B%5D=metric%3Afunction_complexity&cols%5B%5D=metric%3Aclass_complexity&cols%5B%5D=metric%3Afile_complexity&cols%5B%5D=metric%3Acomment_lines_density&cols%5B%5D=metric%3Aduplicated_lines_density&cols%5B%5D=metric%3Ablocker_violations&cols%5B%5D=metric%3Acritical_violations&cols%5B%5D=metric%3Amajor_violations&cols%5B%5D=metric%3Aminor_violations&cols%5B%5D=metric%3Ainfo_violations&cols%5B%5D=metric%3Asqale_index&cols%5B%5D=metric%3Asqale_debt_ratio&cols%5B%5D=metric%3Afiles&cols%5B%5D=metric%3Afunctions&cols%5B%5D=metric%3Aclasses&cols%5B%5D=metric%3Acomplexity&display=list&onBaseComponents=true&pageSize=100&sort=name&id=99&edit=true"


        #"https://sonarqube.com/measures/search/99?asc=true&base=Languages&cols%5B%5D=name&cols%5B%5D=date&cols%5B%5D=metric%3Ancloc&cols%5B%5D=metric%3Aviolations&cols%5B%5D=metric%3Aprojects&cols%5B%5D=metric%3Afunction_complexity&cols%5B%5D=metric%3Aclass_complexity&cols%5B%5D=metric%3Afile_complexity&cols%5B%5D=metric%3Acoverage&cols%5B%5D=metric%3Acomment_lines_density&cols%5B%5D=metric%3Aduplicated_lines_density&cols%5B%5D=metric%3Ablocker_violations&cols%5B%5D=metric%3Acritical_violations&cols%5B%5D=metric%3Amajor_violations&cols%5B%5D=metric%3Aminor_violations&cols%5B%5D=metric%3Ainfo_violations&cols%5B%5D=metric%3Asqale_index&cols%5B%5D=metric%3Asqale_debt_ratio&display=list&onBaseComponents=true&pageSize=100&sort=name&id=99&edit=true"
        self.baixar_arquivo(resumo_page)

        registros = self.get_registros()
        #print "quantas linhas:",len(registros)-1
        linguagens_procuradas = ["JAVA","C++","PYTHON","C","COBOL","JAVASCRIPT","PHP"]
        lista_referencias = []
        for item in registros[1:]:
            linguagem      = self.get_nome_projeto(item)
            if linguagem in linguagens_procuradas:
                referencia = self.obter_referencia(item)
                lista_referencias.append(referencia)

        return lista_referencias

    def obter_referencia(self, registro):
        referencia = Referencia()
        referencia.linguagem = self.get_nome_projeto(registro)
        referencia.total_projetos = formatar_inteiro(self.get_metrica(registro, "m_projects"))

        referencia.linhas_codigo = formatar_inteiro(self.get_metrica(registro, metrica.linhas_codigo))
        referencia.total_linhas = formatar_inteiro(self.get_metrica(registro, metrica.total_linhas))
        referencia.arquivos = formatar_inteiro(self.get_metrica(registro, metrica.arquivos))
        referencia.classes = formatar_inteiro(self.get_metrica(registro, metrica.classes))
        referencia.metodos = formatar_inteiro(self.get_metrica(registro, metrica.metodos))

        referencia.complexidade_total = formatar_inteiro(self.get_metrica(registro, metrica.complexidade_total))
        referencia.complexidade_metodo = self.get_metrica(registro, metrica.complexidade_metodo)
        referencia.complexidade_classe = self.get_metrica(registro, metrica.complexidade_classe)
        referencia.complexidade_arquivo = self.get_metrica(registro, metrica.complexidade_arquivo)

        referencia.taxa_duplicacao = formatar_float(self.get_metrica(registro, metrica.taxa_duplicacao))
        referencia.taxa_divida_tecnica = formatar_float(self.get_metrica(registro, metrica.taxa_divida_tecnica))
        referencia.total_problemas = formatar_inteiro(self.get_metrica(registro, metrica.total_problemas))
        referencia.problemas_criticos = formatar_inteiro(self.get_metrica(registro, metrica.problemas_criticos))
        referencia.problemas_importantes = formatar_inteiro(self.get_metrica(registro, metrica.problemas_importantes))
        referencia.problemas_moderados = formatar_inteiro(self.get_metrica(registro, metrica.problemas_moderados))
        referencia.problemas_normais = formatar_inteiro(self.get_metrica(registro, metrica.problemas_normais))
        referencia.problemas_simples = formatar_inteiro(self.get_metrica(registro, metrica.problemas_simples))

        referencia.taxa_comentarios = formatar_float(self.get_metrica(registro, metrica.taxa_comentarios))
        return referencia
        #referencia.data_revisao = ""

    def exibir_referencia(self):
        print self.linguagem, " - ", self.total_projetos, "Projetos."
        print "COMPLEX. MET: ", self.complexidade_metodo
        print "TAXA DUPLICACAO:", self.taxa_duplicacao
        print "TAXA DIVIDA TECNICA:", self.taxa_divida_tecnica
        print "TAXA COMENTARIOS:", self.taxa_comentarios

    def get_metrica(self, linha, campo):
        try:
            metrica = linha.find("span", {"id": campo}).text
        except:
            metrica = None
        return metrica

    def get_registros(self):
        tabela_metricas = self.arquivo.find('table', {'id': 'measures-table'})
        linhas = tabela_metricas.findAll("tr", {'class': 'highlight'})
        linhas = linhas + tabela_metricas.findAll("tr", {'class': 'odd'})
        linhas = linhas + tabela_metricas.findAll("tr", {'class': 'even'})
        return linhas

    def get_nome_projeto(self, linha):
        try:
            nome = linha.find("a").text
        except:
            nome = ""
        return nome.upper()

def formatar_inteiro(texto):
    try:
        valor = int(texto.replace(",", "").replace(" ",""))

    except:
        print "campo vazio",texto
        valor = None

    return valor

def formatar_float(texto):
    valor = float(texto.replace("%", "").replace(" ", ""))
    try:
        valor = float(texto.replace("%", "").replace(" ", ""))

    except:
        print "campo vazio flost", texto
        valor = None

    return valor



    """
    def coletar(self,link):
        self.baixar_arquivo(link)
        if self.projeto_existe():            
            self.get_dados_identificacao()
            self.get_dados_estrutura()
            self.get_dados_complexidade()
            self.get_dados_duplicacao()
            self.get_dados_problemas()
        else:
            print "Erro! Projeto apagado ou url invalida"
    
    def get_dados_identificacao(self):
        self.get_linguagem_projeto()   
        self.get_nome_projeto()
    
    def get_dados_estrutura(self):
        self.get_metrica(metrica.linhas_codigo)        
        self.get_metrica(metrica.total_linhas)
        self.get_metrica(metrica.arquivos)
        self.get_metrica(metrica.classes)
        self.get_metrica(metrica.metodos)
        
    def get_dados_complexidade(self):
        self.get_metrica(metrica.complexidade_total)
        self.get_metrica(metrica.complexidade_metodo)
        self.get_metrica(metrica.complexidade_classe)
        self.get_metrica(metrica.complexidade_arquivo)
        
    def get_dados_duplicacao(self):
        self.get_metrica(metrica.taxa_duplicacao)
        
    def get_dados_problemas(self):
        self.get_metrica(metrica.taxa_divida_tecnica)
        self.get_metrica(metrica.problemas_criticos)
        self.get_metrica(metrica.problemas_importantes)
        self.get_metrica(metrica.problemas_moderados)
        self.get_metrica(metrica.problemas_normais)
        self.get_metrica(metrica.problemas_simples)
    
    def get_metrica(self,metrica_id):#,block_id_padrao,*args):
        try:
            valor = self.arquivo.find("span",id=metrica_id).contents[0]
            valor = valor.replace(",","")
            valor = valor.replace("%","")
            
        except:
            print "Algum valor nao foi encontrado e foi definido com Zero"
            valor = 0
        
        print "Dado: ",metrica_id," - Valor: ",valor
        return valor
    
    def get_linguagem_projeto(self):
        try:
            valor = self.arquivo.findAll("table",id="size-widget-language-dist")[0].findAll(['td'])[0].contents[0]
        except:
            try:
                div = self.arquivo.find("div",{"class":"block","id":"block_1"})
                valor = div.find("div",{"class":"widget-measure-container"})
                valor = valor.contents[2]
            except:
                return None               
        
        if valor[0] == " ": 
            valor = valor[1:]
            
        valor = valor.replace("\n","")  
        valor = valor.replace("  ","")
        print "Linguagem do Projeto: %s"%valor
        return valor 
            
    def get_nome_projeto(self):
        divs = self.arquivo.findAll("div",id="block_112")
        try:
            if divs != None:
                nome = divs[0].findAll(['h3'])[0].contents[2]
        except:
            divs = self.arquivo.find('div',{'class':'print'})
            print "Olha o queveio: ",divs
            nome = divs.find('h2').contents[0]
            
        
        if nome[0] == " ": 
            nome = nome[1:]
            
        nome = nome.replace("\n","")
        nome = nome.replace("  ","")
        print "Nome do Projeto:",nome
        return nome


    def projeto_existe(self):
        span_error = self.arquivo.find("span",{"id":"errormsg"})
        print span_error
        print "olha o conteudo: >%s<"%(span_error.text)
        if span_error != None:
            return True
        else:
            return False
    
    
    """
    
    
"""    
class VerificadorProjetos():
    
    Arquivo    = None
    LeitorHTML = None
    Projeto    = None    
    
    def __init__(self,*args):
        print "Verificador Construido com Sucesso! \n"
        
        
    def BuscarInformacaoBasica(self,link):
        self.BaixarArquivo(link)
        self.SimplificarDocumento()
        return self.getNomeProjeto(),self.getLinguagemProjeto()
    
    def Analisar(self,Projeto):
        self.BaixarArquivo(Projeto.Link)
        self.SimplificarDocumento()
        
        estado_projeto = Estado()
        estado_projeto.Projeto = Projeto
          
        estado_projeto.NumeroLinhasCodigo     = self.getMetrica("m_ncloc", "block_1")
        estado_projeto.NumeroTotalLinhas      = self.getMetrica("m_lines", "block_1")
        estado_projeto.NumeroClasses          = self.getMetrica("m_classes", "block_1")
        estado_projeto.NumeroArquivos         = self.getMetrica("m_files", "block_1")
        estado_projeto.NumeroMetodos          = self.getMetrica("m_functions", "block_1")
        
        estado_projeto.ComplexidadeTotal      = self.getMetrica("m_complexity", "block_3")
        estado_projeto.ComplexidadePorMetodo  = self.getMetrica("m_function_complexity", "block_3")
        estado_projeto.ComplexidadePorClasse  = self.getMetrica("m_class_complexity", "block_3")
        estado_projeto.ComplexidadePorArquivo = self.getMetrica("m_file_complexity", "block_3")
        
        estado_projeto.TaxaDuplicacao = self.getMetrica("m_duplicated_lines_density","block_437","block_2")
        
        estado_projeto.TaxaDividaTecnica            = self.getMetrica("m_sqale_debt_ratio","block_616","block_6")
        estado_projeto.NumeroProblemasMuitoCriticos = self.getMetrica("m_blocker_violations","block_7")
        estado_projeto.NumeroProblemasCriticos      = self.getMetrica("m_critical_violations","block_7")
        estado_projeto.NumeroProblemasModerados     = self.getMetrica("m_major_violations","block_7")
        estado_projeto.NumeroProblemasNormais       = self.getMetrica("m_minor_violations","block_7")
        estado_projeto.NumeroProblemasSimples       = self.getMetrica("m_info_violations","block_7")
        
        return estado_projeto
    
    def getMetrica(self,metrica_id,block_id_padrao,*args):
        #inicio = time.time()
        try:
            valor = self.Arquivo.find("span",id=metrica_id).contents[0]
            valor = valor.replace(",","")
            valor = valor.replace("%","")
            
        except:
            print "Algum valor nao foi encontrado e foi definido com Zero"
            valor = 0
        
        #duracao = time.time() - inicio
        #print "Consulta em ",duracao
        return valor
    

    def AnalisarProjeto(self,link):
        self.BaixarArquivo(link)
        self.SimplificarDocumento()
        
        self.Projeto               = Projeto(link)
        self.Projeto.Nome          = self.getNomeProjeto()
        self.Projeto.Complexidade  = self.getMetrica("m_function_complexity", "block_3")
        self.Projeto.Duplicacao    = self.getMetrica("m_duplicated_lines_density","block_437","block_2")
        self.Projeto.DividaTecnica = self.getMetrica("m_sqale_debt_ratio","block_616")
        
        texto = "" + "Projeto: "+self.Projeto.Nome+"\n"
        texto = texto + "Complexidade: "+self.Projeto.Complexidade+"\n"
        texto = texto + "Duplicacao: "+self.Projeto.Duplicacao+"\n"
        texto = texto + "Divida Tecnica: "+self.Projeto.DividaTecnica+"\n"
         
        return texto
        
    def getTotalNemoLinks(self):
        self.BaixarArquivo("http://nemo.sonarqube.org/measures/search/68?widget_id=&asc=false&c3_metric=tests&c3_op=eq&cols%5B%5D=metric%3Aalert_status&cols%5B%5D=name&cols%5B%5D=date&cols%5B%5D=metric%3Ancloc&cols%5B%5D=metric%3Aviolations&cols%5B%5D=links&display=list&page=1&pageSize=100&qualifiers%5B%5D=TRK&sort=metric%3Ancloc&id=68")
        self.SimplificarDocumento()
                
        div = self.Arquivo.findAll("div", id="measure_filter_foot_pages")[0].contents[0]
        div = str(div)
        
        resultado = re.search(r'^>*(\d*) results', div).group(1)
        return int(resultado)
            
    def getNemoLinks(self):
        Links = []
        Fonte, Lista = self.getLinks("http://nemo.sonarqube.org/measures/search/68?widget_id=&asc=false&c3_metric=tests&c3_op=eq&cols%5B%5D=metric%3Aalert_status&cols%5B%5D=name&cols%5B%5D=date&cols%5B%5D=metric%3Ancloc&cols%5B%5D=metric%3Aviolations&cols%5B%5D=links&display=list&page=1&pageSize=100&qualifiers%5B%5D=TRK&sort=metric%3Ancloc&id=68")
        Links = Links+Lista
        
        while Fonte != None:
            Fonte, Lista = self.getLinks(Fonte)
            Links = Links+Lista
        return Links              
        
    def getLinks(self,Fonte):
        Links = []
        self.BaixarArquivo(Fonte)
        self.SimplificarDocumento()
                
        div = self.Arquivo.findAll("td",{"class":"nowrap"})
                
        for item in div:
            link = item.findAll("a",href=True,title=True)
            if link != []:  
                Links.append("http://nemo.sonarqube.org"+link[0]['href'])
                #print "Adicionando link: ","http://nemo.sonarqube.org"+link[0]['href']
                
        footer = self.Arquivo.find("tfoot")
       
        list_links = footer.findAll("a",href=True)
        
        url = None
        for link in list_links:
            if "Next" in link:                
                url = "http://nemo.sonarqube.org"+link["href"]
               
        return url,Links
        
  """  
    
    
if __name__=="__main__":
    print "Coletor de Dados (Teste)"
    coletor = coletor_dados()
    coletor.coletar_referencias()
    coletor.coletar_metricas_projetos()
    #coletor.coletar("https://sonarqube.com/dashboard?id=org.apache.abdera%3Aabdera&did=148")
    
        
         
    
    
