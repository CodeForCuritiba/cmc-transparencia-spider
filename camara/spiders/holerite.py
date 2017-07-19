import scrapy
from camara.items import VereadorItem
from scrapy.selector import Selector
import os
import time
import re

BASE_URL = 'https://www.cmc.pr.gov.br/portal-transparencia/'

CPF = os.environ['CMC_CPF']
SENHA = os.environ['CMC_SENHA']
GRUPO = os.environ['CMC_GRUPO']

class HoleriteSpider(scrapy.Spider):
    entities = {}
    headers = []
    name = 'holerite'
    start_urls = [BASE_URL + '/consultante/login.html']

    def parse(self, response):
        """
        The spider init with the login page, and pass the response
        to logged_in to check if is corrected logged in
        """
        return scrapy.FormRequest.from_response(
            response,
            formdata={'con_cpf': CPF, 'con_senha': SENHA},
            callback=self.logged_in
        )

    def logged_in(self, response):
        """
        Check if the user is logged in
        """
        if "Bem vindo," in response.text:
            self.log('Usuário Logado!')
            return self.parse_dates(response)
        else:
            return self.log('Algo deu errado no login')

    def parse_dates(self, response):
        """
        The data is organized by dates, the spider will
        get the entire year relative data
        """
        for date in response.css('select[name="mesano"] option'):
            mesano = date.css('::attr(value)').extract_first()

            if re.search(r"(\d{4})", mesano).group(1) == time.strftime("%Y"):

                request = scrapy.FormRequest(
                    url=BASE_URL + 'holerite/index.html',
                    formdata={
                        'acao': '',
                        'grupo': GRUPO,
                        'mesano': mesano,
                        'tipo': '1'
                    },
                    callback=self.parse_entities
                )

                request.meta['mesano'] = mesano

                yield request

    def parse_entities(self, response):
        """
        A table is displayed with the data about the person
        who works at the Câmara
        """

        mesano = response.meta['mesano']

        self.log('Getting mesano: ' + mesano)

        # Check if the table is empty
        if not response.css('table tr td:nth-child(1)').extract_first():
            return self.log('Nenhum dado disponível')

        for tr in response.xpath('//table/tr').extract():
            selector = Selector(text=tr)
            entity_id = re.search("(javascript:pesquisa\()(\d*)(\);)", tr).group(2)

            request = scrapy.FormRequest(
                url=BASE_URL + 'holerite/consulta_beneficiario.html',
                formdata={
                    'hol_ben_id': entity_id,
                    'hol_mesano': mesano,
                    'hol_tipo': '1',
                    'hol_grupo': GRUPO,
                    'acao':''
                },
                callback=self.parse_salaries
            )

            request.meta['name'] = selector.xpath("//tr/td/text()").extract_first()
            request.meta['entity_id'] = entity_id
            request.meta['mesano'] = mesano

            yield request

    def parse_salaries(self, response):
        """
        The values about person salary is in another table
        in another page, that function grab all the table headers
        and values and assign to the entity[entity_id]
        The id was passed in the response.meta
        """

        item = VereadorItem()
        item['name'] = response.meta['name']
        item['id'] = response.meta['entity_id']
        item['mesano'] = response.meta['mesano']

        for salary in response.xpath('//*[@id="holerite"]').extract():
            selector = Selector(text=salary)
            table = selector.xpath('//tr[@class="holerite_valor"]/td/text()').extract()
            item["salary_gross"] = table[0]
            item["salary_liquid"] = selector.xpath('//tr[@class="holerite_valor"]/td/strong/text()').extract_first()
            return item
