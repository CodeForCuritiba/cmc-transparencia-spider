import scrapy
import os
import datetime

BASE_URL = 'https://www.cmc.pr.gov.br/portal-transparencia/'

CPF = os.environ['CMC_CPF']
SENHA = os.environ['CMC_SENHA']
GRUPO = os.environ['CMC_GRUPO']

NOW = datetime.datetime.now()

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
            if mesano.find(str(NOW.year)) > -1:
                response = scrapy.FormRequest(
                    url=BASE_URL + '/holerite/index.html',
                    formdata={
                        'acao':'',
                        'grupo':GRUPO,
                        'mesano': mesano,
                        'tipo':'1'
                    },
                    callback=self.parse_entities
                )

                response.meta['mesano'] = mesano

                yield response

    def parse_entities(self, response):
        """
        A table is displayed with the data about the person
        who works at the Câmara
        """
        mesano = response.meta['mesano']
        self.log('Getting mesano: ' + str(mesano))

        # Check if the table is empty
        table_empty = not response.css('table tr td:nth-child(1)') \
                                    .extract_first()
        if table_empty:
            return self.log('Nenhum dado disponível')

        # If the headers wasn't defined yet mount the set
        headers_length = len(self.headers)
        if headers_length is 0:
            for th in response.css('table tr th'):
                header = th.css('::text').extract_first()
                if header:
                    self.headers.append(header)
            headers_length = len(self.headers)

        # Get all the values about the entities
        for tr in response.css('table tr'):
            # If row is the header row ignore
            if not tr.css('td'):
                continue

            id_index = str(headers_length + 1)

            # self.log('------------------------------------------------------')
            # self.log(self.headers)
            # self.log('id_index: ' + id_index)
            # self.log(tr.css('td:nth-child('+id_index+')'))
            # return self.log('------------------------------------------------------')

            entity_id = tr.css('td:nth-child('+id_index+') a::attr(href)') \
                            .extract_first() \
                            .replace('javascript:pesquisa(', '') \
                            .replace(');', '')

            # If the entity wasn't found yet get the profile
            if entity_id not in self.entities.keys():
                self.entities[entity_id] = self.__get_entity_profile(tr, entity_id)

            # Make a new request to get salaries in the other page
            request = scrapy.FormRequest(
                url=BASE_URL + '/holerite/consulta_beneficiario.html',
                formdata={
                    'hol_ben_id':entity_id,
                    'hol_mesano':mesano,
                    'hol_tipo':'1',
                    'hol_grupo':GRUPO,
                    'acao':''
                },
                callback=self.parse_salaries
            )

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

        entity_id = response.meta['entity_id']
        mes_ano = response.meta['mesano']
        entity = self.entities.get(entity_id)

        if "Vencimentos pagos pelo órgão de origem." in response.text:
            entity['salaries'][mes_ano] = "Vencimentos pagos pelo órgão de origem."
            yield entity
        elif "Consultado por" not in response.text:
            self.log('-------> ERRO ao consultar salários')
            entity['salaries'][mes_ano] = response.text

        # Init the month salary at the entity
        if mes_ano not in entity.keys():
            entity['salaries'][mes_ano] = {}

        for td in response.css('table tr.holerite_descricao td'):
            header = td.css('::text').extract_first()
            entity['salaries'][mes_ano][header] = ''

        i = 0
        for td in response.css('table tr.holerite_valor td'):
            value = td.css('::text').extract_first()
            keyName = list(entity['salaries'][mes_ano].keys())[i]
            entity['salaries'][mes_ano][keyName] = value
            i += 1

        yield entity

    def __get_entity_profile(self, table_row, entity_id):
        values = {}
        i = 0
        for td in table_row.css('td'):
            try:
                values[self.headers[i]] = td.css('::text') \
                                            .extract_first()
            except IndexError:
                pass
            finally:
                i += 1

        values['id'] = entity_id
        values['salaries'] = {}

        return values