import urllib2

from bs4 import BeautifulSoup


class coletor_dados():
    arquivo = None
    link = None

    # def __init__(self):
    #    print "Coletor construido com sucesso!"

    def baixar_arquivo(self, link):
        conexao = urllib2.urlopen(link)
        self.arquivo = conexao.read()
        self.simplificar_arquivo()

    def simplificar_arquivo(self):
        self.leitor_html = BeautifulSoup(self.arquivo, "html5lib")
        self.arquivo = self.leitor_html.find('div', {'id': 'body'})

    def coletar_dados_repositorio(self,url_repositorio):
        if url_repositorio[-1] == '/':
            page = url_repositorio+"measures/filter/1"
        else:
            page = url_repositorio + "/measures/filter/1"
        print "Olha a url: ",page
        self.baixar_arquivo(page)
        registros = self.get_registros()

        lista_dados = []
        for item in registros:
            lista_dados.append(self.get_nome(item))
        return lista_dados

    def get_registros(self):
        tabela_metricas = self.arquivo.find('table', {'id': 'measures-table'})
        linhas = tabela_metricas.findAll("tr", {'class': 'highlight'})
        linhas = linhas + tabela_metricas.findAll("tr", {'class': 'odd'})
        linhas = linhas + tabela_metricas.findAll("tr", {'class': 'even'})
        return linhas

    def get_nome(self, registro):
        linha = registro.find("a")
        url_projeto = linha['href']
        nome_projeto = linha['title']
        return nome_projeto,url_projeto

    def coletar_dados_projetos(self,):
        resumo_page = "http://localhost:9000/measures/search/1?asc=true&cols%5B%5D=metric%3Aalert_status&cols%5B%5D=name&cols%5B%5D=metric%3Alines&cols%5B%5D=metric%3Ancloc&cols%5B%5D=metric%3Afunction_complexity&cols%5B%5D=metric%3Aclass_complexity&cols%5B%5D=metric%3Afile_complexity&cols%5B%5D=metric%3Acomment_lines_density&cols%5B%5D=metric%3Aduplicated_lines_density&cols%5B%5D=metric%3Aviolations&cols%5B%5D=metric%3Ablocker_violations&cols%5B%5D=metric%3Acritical_violations&cols%5B%5D=metric%3Amajor_violations&cols%5B%5D=metric%3Aminor_violations&cols%5B%5D=metric%3Ainfo_violations&cols%5B%5D=metric%3Asqale_index&cols%5B%5D=metric%3Asqale_debt_ratio&cols%5B%5D=metric%3Acode_smells&display=list&pageSize=100&qualifiers=TRK&sort=name&id=1&edit=true"
        self.baixar_arquivo(resumo_page)
        registros = self.get_registros()
        for item in registros:
            print item
