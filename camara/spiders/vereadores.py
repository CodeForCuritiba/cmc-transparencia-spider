import scrapy
import os

BASE_URL='https://www.cmc.pr.gov.br/portal-transparencia/'
CPF=os.environ['CMC_CPF']
SENHA=os.environ['CMC_SENHA']
vereadores = {}

class VereadoresSpider(scrapy.Spider):
    name = 'vereadores'
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
                formdata={'acao':'', 'grupo':'1', 'mesano': '05/2017', 'tipo':'1'},
                callback=self.parse_vereadores
            )]
        else:
            self.log('Algo deu errado no login')
            return

    def parse_vereadores(self, response):
        # self.log(response.text)
        for tr in response.css('table#beneficiarios tr'):
            nome = tr.css('td::text').extract_first()

            if type(nome) is not str:
                continue

            id = tr.css('a::attr(href)').extract_first().replace('javascript:pesquisa(', '').replace(');', '')
            vereadores[id] = { 'nome': nome }

            request = scrapy.FormRequest(
                    url=BASE_URL + '/holerite/consulta_beneficiario.html',
                    formdata={ 'hol_ben_id':id, 'hol_mesano':'05/2017', 'hol_tipo':'1', 'hol_grupo':'1', 'acao':'' },
                    callback=self.parse_salarios
                )
            request.meta['vereador_id'] = id
            yield request

    def parse_salarios(self, response):
        id = response.meta['vereador_id']
        vereador = vereadores.get(id)
        self.log('Consultando vereador: ' + vereador['nome'])

        if "Consultado por" not in response.text:
            self.log('-------> ERRO ao consultar salários')
            return

        subsidio = response.css('table#holerite tr:nth-child(2) td:nth-child(1)::text').extract_first()
        totalBruto = response.css('table#holerite tr:nth-child(2) td:nth-child(6)::text').extract_first()
        totalDescontos = response.css('table#holerite tr:nth-child(4) td:nth-child(5)::text').extract_first()
        totalLiquido = response.css('table#holerite tr:nth-child(4) td:nth-child(6) strong::text').extract_first()

        vereador['subsidio'] =  subsidio
        vereador['totalBruto'] =  totalBruto
        vereador['totalDescontos'] = totalDescontos
        vereador['totalLiquido'] =  totalLiquido

        yield vereador
