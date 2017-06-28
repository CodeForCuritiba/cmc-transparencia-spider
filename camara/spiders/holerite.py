import scrapy
import os

BASE_URL='https://www.cmc.pr.gov.br/portal-transparencia/'

CPF=os.environ['CMC_CPF']
SENHA=os.environ['CMC_SENHA']
GRUPO=os.environ['CMC_GRUPO']
MESANO=os.environ['CMC_MESANO']

servidores = {}

class HoleriteSpider(scrapy.Spider):
    name = 'holerite'
    start_urls = [BASE_URL + '/consultante/login.html']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'con_cpf': CPF, 'con_senha': SENHA},
            callback=self.logged_in
        )

    def logged_in(self, response):
        if "Bem vindo," in response.text:
            self.log('Usuário Logado!')
            return [scrapy.FormRequest(
                url=BASE_URL + '/holerite/index.html',
                formdata={'acao':'', 'grupo':GRUPO, 'mesano': MESANO, 'tipo':'1'},
                callback=self.parse_servidores
            )]
        else:
            self.log('Algo deu errado no login')
            return

    def parse_servidores(self, response):
        for tr in response.css('table#beneficiarios tr'):
            nome = tr.css('td::text').extract_first()

            if type(nome) is not str:
                continue

            id = tr.css('a::attr(href)').extract_first().replace('javascript:pesquisa(', '').replace(');', '')
            cargo = tr.css('td:nth-child(2)::text').extract_first()
            lotacao = tr.css('td:nth-child(4)::text').extract_first()

            servidores[id] = { 'nome': nome, 'cargo': cargo, 'lotacao': lotacao }

            request = scrapy.FormRequest(
                    url=BASE_URL + '/holerite/consulta_beneficiario.html',
                    formdata={ 'hol_ben_id':id, 'hol_mesano':MESANO, 'hol_tipo':'1', 'hol_grupo':GRUPO, 'acao':'' },
                    callback=self.parse_salarios
                )
            request.meta['ref_id'] = id
            # return request
            yield request

    def parse_salarios(self, response):
        id = response.meta['ref_id']
        servidor = servidores.get(id)
        self.log('Consultando servidor: ' + servidor['nome'])

        if "Consultado por" not in response.text:
            self.log('-------> ERRO ao consultar salários')
            return

        servidor['values'] = {}

        i = 0
        for td in response.css('table tr.holerite_descricao td'):
            header = td.css('::text').extract_first()
            servidor['values'][i] = { 'name': header }
            i += 1

        i = 0
        for td in response.css('table tr.holerite_valor td'):
            value = td.css('::text').extract_first()
            servidor['values'][i]['value'] = value
            i += 1

        yield servidor
