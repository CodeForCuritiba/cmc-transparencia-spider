<center>
<img src="https://github.com/CodeForCuritiba/cmc-transparencia/raw/master/assets/og-image.png" >
</center>

# CMC Transparência

Project to transform the data of "Portal da Transparência" of Câmara Munipal de Curitiba into a user-friendly and anonymously data.

This project was made with `python3` and `scrapy`.

## Dependencies

`pip install Scrapy`

## Grupo de Servidores

    [
        { id: 1, name: 'Vereadores' },
        { id: 2, name: 'Efetivos' },
        { id: 3, name: 'Comissionados' },
        { id: 4, name: 'Inativos' },
        { id: 5, name: 'Ouvidor' },
        { id: 6, name: 'Cedido para a Câmara' },
        { id: 7, name: 'Cedido pela Câmara' },
        { id: 8, name: 'Temporário' },
        { id: 9, name: 'Estagiário' },
    ]

## Running the project

The results will be imported to MongoDB so you need to setup the MongoDB uri:

    export MONGO_URI='mongodb://<user>:<pass>@<server>/<database>'
    export MONGO_DATABASE='<database>'

So you'll able to run the spider:

    CMC_CPF={CPF} CMC_SENHA={SENHA} CMC_GRUPO=1 scrapy crawl holerite
    CMC_CPF={CPF} CMC_SENHA={SENHA} CMC_GRUPO=2 scrapy crawl holerite
    CMC_CPF={CPF} CMC_SENHA={SENHA} CMC_GRUPO=3 scrapy crawl holerite
    CMC_CPF={CPF} CMC_SENHA={SENHA} CMC_GRUPO=4 scrapy crawl holerite
    CMC_CPF={CPF} CMC_SENHA={SENHA} CMC_GRUPO=5 scrapy crawl holerite
    CMC_CPF={CPF} CMC_SENHA={SENHA} CMC_GRUPO=6 scrapy crawl holerite
    CMC_CPF={CPF} CMC_SENHA={SENHA} CMC_GRUPO=7 scrapy crawl holerite
    CMC_CPF={CPF} CMC_SENHA={SENHA} CMC_GRUPO=8 scrapy crawl holerite
    CMC_CPF={CPF} CMC_SENHA={SENHA} CMC_GRUPO=9 scrapy crawl holerite
